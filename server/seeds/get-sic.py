import urllib3
import time
import random
import json
from app import app
from models import Company
from config import app, db, api

proxy_url = 'http://cneeyhab:bdo8b3zg5pcd@38.154.227.167:5868'

http = urllib3.PoolManager()

headers = {'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'
            }

company_batch = []
company_tracker = {}
company_count = 0

with app.app_context():
    
    companies = Company.query.all()

    for company in companies:
        try:
            r = http.request('GET',f"https://data.sec.gov/submissions/CIK{company.cik_10}.json",headers=headers)
            print(f'{companies.index(company)+1}/{len(companies)+1}')
            
            co_json = json.loads(r.data)
            
            company.name = str(co_json.get('name', ''))
            company.sic = int(co_json.get('sic', 0))
            company.sic_description = str(co_json.get('sicDescription', ''))
            company.owner_org = str(co_json.get('ownerOrg', ''))
            company.entity_type = str(co_json.get('entityType', ''))
            
            print(f'{company.name} - {company.sic_description}')

            company_batch.append(company)

            if len(company_batch) >= 500:
                db.session.add_all(company_batch)
                db.session.commit()
                company_batch.clear()
                print("Committed 500 companies to DB.")

        except ValueError as e:
            print(e)
        
        time.sleep(random.uniform(1.03, 1.11))
    
        company_count += 1
        company_tracker[company_count] = company.cik
    
    if len(company_batch) > 0:
        db.session.add_all(company_batch)
        db.session.commit()
        print("Committed remaining companies to DB.")