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
    
    def get_shares(data, company):
            common_shares = CommonShares(company_id = company.id)
            shares_path = ""
            
            try:
                if data.get('facts').get('us-gaap').get('WeightedAverageNumberOfSharesOutstandingBasic').get('units').get('shares'):
                    shares_path = data['facts']['us-gaap']['WeightedAverageNumberOfSharesOutstandingBasic']['units']['shares']
                elif data.get('facts').get('dei').get('EntityCommonStockSharesOutstanding').get('units').get('shares'):
                    shares_path = data['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares']
               

                shares_len = len(shares_path)
                shares = shares_path[shares_len-1].get('val')
                date = shares_path[shares_len-1].get('end')

                common_shares.historical_shares = shares
                common_shares.date = date
                
                print(common_shares.company_id, common_shares.historical_shares)
            
            except Exception as e:
                print(str(e))
            
            shares_path = ""

            try:
                if data.get('facts').get('us-gaap').get('WeightedAverageNumberOfDilutedSharesOutstanding').get('units').get('shares'):
                    shares_path = data['facts']['us-gaap']['WeightedAverageNumberOfDilutedSharesOutstanding']['units']['shares']
                
                shares_len = len(shares_path)
                shares = shares_path[shares_len-1].get('val')
                date = shares_path[shares_len-1].get('end')

                if common_shares.date == None:
                    common_shares.date = date
                
                common_shares.historical_shares_diluted = shares
                print(common_shares.company_id, common_shares.historical_shares_diluted)
            
            except Exception as e:
                print(str(e))
                
                
            batch.append(common_shares)
        

    for company in companies:
        db.session.refresh(company)
        file_path = f'json/CIK{company.cik_10}.json'
        data = json.load(open(file_path, 'r'))
        get_shares(data, company)

    db.session.add_all(batch)    
    db.session.commit()

       

