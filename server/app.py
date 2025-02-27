#!/usr/bin/env python3

# Standard library imports

# Remote library imports
# from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from models import Company, Keyword, company_keyword_assoc, Note, BalanceSheet, IncomeStatement, CashFlowsStatement, CommonShares, CoKeyAssoc
from sqlalchemy import not_, or_
import json
import os
from datetime import datetime, timedelta
import time
import requests
from dotenv import load_dotenv
from flask_cors import CORS
# Local imports
from config import app, db, api

@app.route('/companies/<string:ticker>', methods=['GET'])
def get_company(ticker):
    print(ticker)
    try:
        company = Company.query.filter(Company.ticker == ticker.upper()).first()
        return jsonify(company.to_dict()), 200
    except Exception as e:
        return{'error': str(e)}, 404


@app.route('/shares/<int:id>', methods=['GET'])
def get_shares(id):
    shares = CommonShares.query.filter(CommonShares.company_id == id).all()
    if not shares:
        return jsonify({"error": "Shares not found"}), 404
    return jsonify([sh.to_dict() for sh in shares]), 200


@app.route('/balance_sheets/<int:cik>', methods=['GET'])
def get_balancesheets(cik):
    balance_sheets = BalanceSheet.query.filter(BalanceSheet.company_cik == cik,
                                               ).order_by(BalanceSheet.end).all()
    if not balance_sheets:
        return jsonify({"error": "Balance sheets not found"}), 404
    return jsonify([bs.to_dict() for bs in balance_sheets]), 200


@app.route('/income_statements/<int:cik>', methods=['GET'])
def get_income_statements(cik):
    income_statements = IncomeStatement.query.filter(IncomeStatement.company_cik == cik, 
                                                     (IncomeStatement.period_days < 120) | (IncomeStatement.period_days == None)
                                                     ).order_by(IncomeStatement.end).all()
    if not income_statements:
        return jsonify({"error": "Balance sheets not found"}), 404
    return jsonify([income_statement.to_dict() for income_statement in income_statements]), 200


@app.route('/cf_statements/<int:cik>', methods=['GET'])
def get_cf_statements(cik):
    cf_statements = CashFlowsStatement.query.filter(CashFlowsStatement.company_cik == cik, 
                                                     CashFlowsStatement.frame.like('%Q%')
                                                     ).order_by(CashFlowsStatement.end).all()
    if not cf_statements:
        return jsonify({"error": "Balance sheets not found"}), 404
    return jsonify([cf_statement.to_dict() for cf_statement in cf_statements]), 200


@app.get('/companyfacts2/<string:ticker>')
def get_companyfacts_ticker(ticker):
    company = Company.query.filter(Company.ticker == ticker.upper()).first()
    file_path = f'json/CIK{company.cik_10}.json'
    with open(file_path, 'r') as file:
        data = file.read()
    return data, 200, {'Content-Type': 'application/json'}


@app.route('/quotes/<string:ticker>', methods=['GET'])
def get_quotes(ticker: str):
    f_ticker = ticker.replace("-", ".")
    print(f_ticker)
    
    headers = {
            "Content-Type" : "application/json",
            "Accept" : "application/json",
            'APCA-API-KEY-ID': os.getenv('APCA_API_KEY_ID'),
            'APCA-API-SECRET-KEY': os.getenv('APCA_API_SECRET_KEY')
        }

    start = datetime.now() - timedelta(hours=72)
    f_start = start.isoformat() + "Z"
   
    r = requests.get(f'https://data.alpaca.markets/v2/stocks/bars?symbols={f_ticker}&timeframe=1Day&start={f_start}&limit=1000&adjustment=raw&feed=sip&sort=desc', headers=headers)
    
    if not r.ok:
        return "Quote could not be retrieved", r.status_code
    return jsonify(r.json()), r.status_code


@app.route('/keywords', methods=['GET'])
def get_all_keywords():
    keywords = Keyword.query.all()
    if not keywords:
        return jsonify({'error': 'keywords not found'}), 404
    keyword_list = sorted([keyword.to_dict() for keyword in keywords], key=lambda x:x['word'].lower())
    return jsonify(keyword_list), 200


@app.route('/association', methods=['POST'])
def set_association():
    data = request.json
    c_id = int(data[0])
    k_id = int(data[1])
    con = data[2]
    company = db.session.get(Company, c_id)
    keyword = db.session.get(Keyword, k_id)
    
    assoc = CoKeyAssoc.query.filter(CoKeyAssoc.company_id==c_id, CoKeyAssoc.keyword_id==k_id).first()
    
    if assoc and len(assoc.context) > 0:
        print(assoc)
        assoc.context = assoc.context + [con]
    else:
        assoc = CoKeyAssoc(company_id=c_id, keyword_id=k_id, context=[con])

    db.session.add(assoc)
    db.session.commit()
    return jsonify(f'Successfully added {keyword.word} to {company.name}'), 200

@app.route('/api/companies/search', methods=['GET'])
def search_companies():
    query = request.args.get('query', '')
    if query:
        companies = Company.query.filter(
            or_(
                Company.ticker.ilike(f'%{query}%'),
                Company.name.ilike(f'%{query}%')
            )
        ).limit(10).all()
        return jsonify([company.to_dict() for company in companies]), 200 
    return jsonify([]), 400

@app.route('/filings/<string:cik_10>')
def get_filings(cik_10:str):

    
    company = Company.query.filter(Company.cik_10 == cik_10).first()
    
    headers = {
        'User-Agent':'Raymond Michetti michetti.ray@gmail.com'
    }
    
    r = requests.get(f'https://data.sec.gov/submissions/CIK{cik_10}.json', headers=headers)

    if not r.ok:
        return jsonify([]), r.status_code
    
    data = json.loads(r.content)

    all_filings = {
        'latest':[],
        'fin':[],
        'insiders':[],
        'institutions':[]
    }

    try:
        i = 0
        recent_filings = data.get('filings', {}).get('recent', {})
        
        while i < len(recent_filings.get('form', [])):
            form = recent_filings.get('form', [])[i]
            accn = recent_filings.get('accessionNumber', [])[i]
            doc = recent_filings.get('primaryDocument', [])[i]
            reportDate = recent_filings.get('reportDate', [])[i]
            filing = {
                'form' : form,
                'accn' : accn,
                'doc' : doc,
                'url' : "",
                'reportDate': reportDate
            }
            date_str = data.get('filings', {}).get('recent', {}).get('acceptanceDateTime', [])[i]
            formatted_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M')
            filing['date'] = formatted_date
            filing['accn'] = filing['accn'].replace("-", "")
            filing['url'] = f"https://www.sec.gov/Archives/edgar/data/{company.cik}/{filing['accn']}/{filing['doc']}"
            f = filing['form']
            
            # print(filing)
            # print(i)
            
            if form in ("8-K", "6-K", "8-K/A", "6-K/A"):
               filing['form'] = "Form" + " " + form

            if i < 5:
                all_filings['latest'].append(filing)

            if len(all_filings['fin']) < 5:
                if form in ("10-K", "10-K/A", "10-Q", "10-Q/A", "20-F", "20-F/A"):
                    filing['form'] = f'Form {f}'
                    all_filings['fin'].append(filing)

            if len(all_filings['insiders']) < 5:
                if form in ("3", "4", "144", "3/A", "4/A", "144/A"):
                    filing['form'] = f'Form {f}'
                    all_filings['insiders'].append(filing)

            
            if len(all_filings['institutions']) < 5:
                if form in ("SCHEDULE 13G", "SCHEDULE 13D", "SC 13G", "SC 13G/A", "SCHEDULE 13G/A", "SCHEDULE 13D/A",):
                    all_filings['institutions'].append(filing)
            
            if len(all_filings['latest']) + len(all_filings['fin']) + len(all_filings['insiders']) + len(all_filings['institutions']) == 20:
                return jsonify(all_filings), r.status_code
            
            i += 1

        return jsonify(all_filings), r.status_code
    
    except Exception as e:
        return jsonify(all_filings), r.status_code
    

    
    

# app.route('/news', methods=['GET'])
# def get_news():
#     news_key = os.getenv('NEWS_API')
#     proxies = {
#         'http':os.getenv('PROXY_2')
#     }
#     headers = {
#         'Accept': 'content/json',
#         'Content-Type': 'content/json',
#         'x-api-key':news_key
#     }
#     try:
#         r = requests.get(f'https://newsapi.org/v2/top-headalines?country=us&pageSize=100', proxies=proxies, headers=headers)
#         if not r.ok:
#             return jsonify({
#                 'statusCode': r.status_code,
#                 'message': r.json()
#             })
#     except Exception as e:
#         print(str(e))


# @app.post('/companies')
# def post_companies():
#     try:    
#         data = request.json
#         companies = [Company(cik=company[0], name=company[1], ticker=company[2], exchange=company[3]) for company in data['companies']]
#         db.session.add_all(companies)
#         db.session.commit()
#         return {'success': 'companies posted'},200
#     except Exception as e:
#         return {'error': str(e)}, 400


# @app.route('/companies', methods=['POST'])
# def get_company2():
#     data = request.json
#     try:
#         company = Company.query.filter(Company.ticker == data.upper()).first()
#         return jsonify(company.to_dict()), 200
#     except Exception as e:
#         return{'error': str(e)}, 404

    
if __name__ == '__main__':
    load_dotenv()
    app.run(port=5555, debug=True)
    
