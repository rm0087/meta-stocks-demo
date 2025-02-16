import requests
import json
from models import db, Company
from app import app

headers = {
    "Content-Type":"application/json",
    "Accept":"application/json",
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'
}

r = requests.get(url="https://www.sec.gov/files/company_tickers.json", headers=headers)
print(r.status_code)
response = r.json()

ciks = set()
with app.app_context():

    db.session.query(Company).delete()
    db.session.commit()

    for company in response.values():
        if company['cik_str'] not in ciks:
            new_co = Company(
                cik = int(company.get('cik_str')),
                ticker = company.get('ticker'),
                name = company.get('title')
            )

            if len(str(company['cik_str'])) < 10:
                diff = 10 - len(str(company['cik_str']))
                new_co.cik_10 = f"{'0' * diff}{new_co.cik}"

            ciks.add(company['cik_str'])
            db.session.add(new_co)
            db.session.commit()
   

        
