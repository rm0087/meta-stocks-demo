import urllib3
import time
import random
import os
from app import app
from models import Company
import requests
from dotenv import load_dotenv
load_dotenv()
# import json

main_keys = [
   'NetIncomeLoss',
   'NetIncomeLossAvailableToCommonStockholdersBasic',
   'ComprehensiveIncomeAttributableToOwnersOfParent',
   'Revenues',
   'RevenueFromContractWithCustomerExcludingAssessedTax',
   'OperatingIncomeLoss'
]

headers = {
    'User-Agent': 'Raymond Michetti michetti.ray@gmail.com',  # Replace with your details
    # 'Host': 'data.sec.gov',
    # 'Accept-Encoding': 'gzip, deflate',
    # 'Accept' : 'application/json'
}

proxy1 = os.getenv('PROXY_1')
proxies = {
    'https': proxy1
}

def get_company_jsons():
    company_tracker = {}
    company_count = 0

    with app.app_context():
        
        companies = Company.query.all()

        for company in companies:
            if company.cik not in company_tracker.values():
                r = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{company.cik_10}.json",headers=headers)
                
                print(r.data)
                print(f'{company.id}/{len(companies)}')
                
                full_path = os.path.join('json', f'CIK{company.cik_10}.json')
                f = open(full_path, 'wb')
                f.write(r.data)
                f.close()
            else:
                pass
                
            time.sleep(random.uniform(.5, .75))
            
            company_count += 1
            company_tracker[company_count] = company.cik

if __name__ == '__main__':
    count = 1
    for key in main_keys:
        year = 2008
        while year <= 2024:
            q = 1
            while q <= 4:
                # print(f'https://data.sec.gov/api/xbrl/frames/us-gaap/{key}/USD/CY{year}Q{q}.json')
                r = requests.get(url=f'https://data.sec.gov/api/xbrl/frames/us-gaap/{key}/USD/CY{year}Q{q}.json', headers=headers)
                print(count, key, year, f'q{q}')
                print("    Status code:", r.status_code, r.reason)
                # print(r.content)
                full_path = os.path.join('acct-jsons', f'{key}-CY{year}Q{q}I.json')
                with open(full_path, 'wb') as f:
                    f.write(r.content)
                    f.close()
                
                
                q += 1
                count += 1

                time.sleep(random.uniform(1.1, 2.3))
            year += 1


