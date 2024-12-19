#!/usr/bin/env python3

# Standard library imports

# Remote library imports
# from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from models import Company, Keyword, company_keyword_assoc, Note, BalanceSheet, IncomeStatement, CashFlowsStatement, CommonShares
from sqlalchemy import not_, or_
import json
import os
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

# Local imports
from config import app, db, api

load_dotenv()

@app.post('/companies')
def get_all_companies():
    data = request.json
    try:
        company = Company.query.filter(Company.ticker == data.upper()).first()
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
    balance_sheets = BalanceSheet.query.filter(BalanceSheet.company_cik == cik
                                               ).order_by(BalanceSheet.end).all()
    if not balance_sheets:
        return jsonify({"error": "Balance sheets not found"}), 404
    return jsonify([bs.to_dict() for bs in balance_sheets]), 200

@app.route('/income_statements/<int:cik>', methods=['GET'])
def get_income_statements(cik):
    income_statements = IncomeStatement.query.filter(IncomeStatement.company_cik == cik, 
                                                     IncomeStatement.frame.like('%Q%')
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


app.route('/news', methods=['GET'])
def get_news():
    news_key = os.getenv('NEWS_API')
    
    proxies = {
        'http':os.getenv('PROXY_2')
    }

    headers = {
        'Accept': 'content/json',
        'Content-Type': 'content/json',
        'x-api-key':news_key
    }

    try:
        r = requests.get(f'https://newsapi.org/v2/top-headalines?country=us&pageSize=100', proxies=proxies, headers=headers)
        
        if not r.ok:
            return jsonify({
                'statusCode': r.status_code,
                'message': r.json()
            })
    except Exception as e:
        print(str(e))

















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
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)

