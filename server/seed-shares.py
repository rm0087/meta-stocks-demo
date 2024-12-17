import time
from random import randint
import os
import json
from app import app
from models import db, Company, CommonShares




batch = []

with app.app_context():
    db.session.query(CommonShares).delete()
    db.session.commit()
    companies = Company.query.all()
    for company in companies:
        db.session.refresh(company)
        file_path = f'json/CIK{company.cik_10}.json'
        data = json.load(open(file_path, 'r'))
        shares_path = ""

        try:
            if data.get('facts').get('dei').get('EntityCommonStockSharesOutstanding').get('units').get('shares'):
                shares_path = data.get('facts').get('dei').get('EntityCommonStockSharesOutstanding').get('units').get('shares')
            elif data.get('facts').get('us-gaap').get('CommonStockSharesOutstanding').get('units').get('shares'):
                shares_path = data.get('us-gaap').get('dei').get('CommonStockSharesOutstanding').get('units').get('shares')

            shares_len = len(shares_path)
            shares = shares_path[shares_len-1].get('val')
            date = shares_path[shares_len-1].get('end')
            
            new = CommonShares(company_id = company.id, historical_shares = shares, date=date)
            print(new.company_id, new.historical_shares)
            batch.append(new)
        except:
            pass
    db.session.add_all(batch)    
    db.session.commit()

       

