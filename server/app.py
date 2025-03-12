#!/usr/bin/env python3

# Standard library imports

# Remote library imports
# from flask_migrate import Migrate
import re
import markdown
from urllib.parse import unquote
import anthropic
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from models import Company, Keyword, company_keyword_assoc, AISummary, Note, BalanceSheet, IncomeStatement, CashFlowsStatement, CommonShares, CoKeyAssoc
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

def filter_encoded_images(text):
    # Pattern to match uuencoded files
    # This matches content starting with "begin" and ending with "end"
    uuencode_pattern = re.compile(r'<TEXT>\s*begin\s+\d+\s+\S+\s+[\s\S]*?end\s*</TEXT>', re.MULTILINE)
    
    # Filter out the encoded image sections
    filtered_text = uuencode_pattern.sub('', text)
    
    return filtered_text

def remove_encoded_blocks(text):
    # Remove content between <TEXT> tags that appears to be encoded
    text_tag_pattern = r'<TEXT>\s*begin [^<]+</TEXT>'
    
    # Replace with a placeholder
    cleaned_text = re.sub(text_tag_pattern, '<TEXT>[ENCODED CONTENT REMOVED]</TEXT>', text, flags=re.DOTALL)
    
    return cleaned_text
def clean_encoded_content(text):
    patterns = [
        # UUEncoded content
        r'begin \d+ [^\n]+\.[a-zA-Z0-9]+\n(?:[M-_][^\n]*\n)+(?:end|`)',
        
        # Base64 encoded data (common patterns)
        r'data:[^;]+;base64,[a-zA-Z0-9+/=]+',
        
        # Long strings of seemingly random characters that might be encoded data
        r'(?:[A-Za-z0-9+/=]{50,})',
        
        # Hexadecimal data dumps
        r'(?:(?:[0-9A-F]{2}\s){8,}(?:[0-9A-F]{2}))',
    ]
    
    cleaned_text = text
    for pattern in patterns:
        cleaned_text = re.sub(pattern, '[BINARY CONTENT REMOVED]', cleaned_text, flags=re.DOTALL)
    
    return cleaned_text

def normalize_whitespace(text):
    # Replace multiple whitespace characters with a single space
    normalized_text = re.sub(r'\s+', ' ', text)
    # Remove leading and trailing whitespace
    normalized_text = normalized_text.strip()
    return normalized_text

def remove_html_tags(html_text):
    # Remove HTML tags
    clean_text = re.sub(r'<.*?>', '', html_text)
    
    # Optional: Replace multiple whitespaces with a single space
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    return clean_text


def remove_binary_content(text):
    # Pattern to match uuencoded content (begins with "begin" and contains encoded lines)
    uuencode_pattern = r'begin \d+ [^\n]+\.jpg\n(?:[M-_][^\n]*\n)+(?:end|`)'
    
    # Remove uuencoded content
    cleaned_text = re.sub(uuencode_pattern, '[IMAGE CONTENT REMOVED]', text, flags=re.DOTALL)
    
    return cleaned_text

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
                                                     (IncomeStatement.period_days < 120) | (IncomeStatement.period_days == None), 
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
            txt = accn + ".txt"
            url_prefix = f"https://www.sec.gov/Archives/edgar/data/{company.cik}/"
            url_suffix = accn.replace("-", "") + "/"
            url = url_prefix + url_suffix
            date_str = data.get('filings', {}).get('recent', {}).get('acceptanceDateTime', [])[i]
            formatted_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M') 

            filing = {
                'form' : form,
                'accn' : accn,
                'filingDate' : formatted_date,
                'reportDate': reportDate,
                'fullFilingUrl': url + accn + "-index.html",
                'doc' : doc,
                'urlPrefix' : url,
                'txt' : txt,
            }
            
            f = filing['form']
            
            if form in ("8-K", "6-K", "8-K/A", "6-K/A"):
               filing['form'] = "Form" + " " + form
            
            if i < 30:
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
            
            if len(all_filings['latest']) + len(all_filings['fin']) + len(all_filings['insiders']) + len(all_filings['institutions']) == 45:
                return jsonify(all_filings), r.status_code
            
            i += 1

        return jsonify(all_filings), r.status_code
    
    except Exception as e:
        return jsonify(all_filings), r.status_code
    
@app.route('/ai/analyze', methods=["GET"])
def get_ai_analysis():
    txt_url = request.args.get('url', '')
    unq_url = unquote(txt_url)
    decoded_url = unq_url
    cik2 = re.sub(r'^https://www.sec.gov/Archives/edgar/data/([^/]*)(?:/.*)?$', r'\1', decoded_url)
    
    print("Initiating LLM request.")
    with app.app_context():
        summary = AISummary.query.filter(AISummary.url == decoded_url).first()
        if summary:
            print("Local AI summary found. Request complete.")
            return jsonify(summary.to_dict()), 200

    headers = {
        'User-Agent': 'Raymond Michetti michetti.ray@gmail.com'
    }

    try:
        response = requests.get(decoded_url, headers=headers)
        
        if response.status_code != 200:
            return jsonify({
                "error": f"Failed to retrieve content: HTTP {response.status_code}"
            }), 500
        
        print("Encoding request.")
        raw_txt = response.text
        content = filter_encoded_images(raw_txt)
        # print(content)
        
        print("Sending request to LLM. Awaiting response...")
        client = anthropic.Anthropic(
            api_key= os.getenv('CLAUDE_KEY')
        )
    
        summary_text = ""
        with client.messages.stream(
                # model="claude-3-7-sonnet-20250219",
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": f'Please summarize following SEC document: {content}'
                    }
                ]
            ) as stream:
                print('Response: ', stream.response)
                for text in stream.text_stream:
                    summary_text += text
                
                final_message = stream.get_final_message()
        
                summary_response = {
                    "summary": markdown.markdown(summary_text),
                    "model": final_message.model,
                    "usage": {
                        "input_tokens": final_message.usage.input_tokens,
                        "output_tokens": final_message.usage.output_tokens
                    },
                    "original_url": decoded_url,
                    "content_length": len(content)
                }

                with app.app_context():
                    new_ai = AISummary(
                        co_cik = cik2,
                        url = summary_response['original_url'],
                        content_length = summary_response['content_length'],
                        summary = summary_response['summary'],
                        model = summary_response['model'],
                        input_tokens = summary_response['usage']['input_tokens'],
                        output_tokens = summary_response['usage']['output_tokens'],
                    )
                    db.session.add(new_ai)
                    db.session.commit()
                    print("LLM request complete.")
                    return jsonify(new_ai.to_dict()), 200
        
    except requests.RequestException as e:
        return jsonify({
            "error": f"Failed to retrieve content: {str(e)}"
        }), 500
    
  
if __name__ == '__main__':
    load_dotenv()
    app.run(port=5555, debug=True)


##### ARCHIVED ##############
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
    
