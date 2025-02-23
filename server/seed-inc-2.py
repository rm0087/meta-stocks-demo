#!/usr/bin/env python3
import math
import time
from datetime import datetime
start_time = time.time()
from random import randint
import os
import json
from app import app
from models import db, Company, IncomeStatement
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

## DEFINITIONS BEGIN #####################################################################################################
main_keys = [
   'NetIncomeLoss',
   'NetIncomeLossAvailableToCommonStockholdersBasic',
   'ComprehensiveIncomeAttributableToOwnersOfParent',
]

all_keys =  [  
   # 'Revenues',
   # 'RevenueFromContractWithCustomerExcludingAssessedTax', 
   # 'RevenuesNetOfInterestExpense', 
   # 'RevenueFromContractWithCustomerIncludingAssessedTax', 
   # 'SalesRevenueNet',
   # 'SalesRevenueGoodsNet', 
   # 'SalesRevenueServicesNet',
   # 'InterestAndDividendIncomeOperating',
   # 'Revenue',
   # 'RevenueFromContractsWithCustomers',
   # 'PreferredStockDividendsIncomeStatementImpact',
   # 'EarningsPerShareBasic'
]

NET_INCOME_KEYS = {
   'NetIncomeLoss':'net_income',
   'NetIncomeLossAvailableToCommonStockholdersBasic':'net_income',
   'ComprehensiveIncomeAttributableToOwnersOfParent':'net_income',
}

REV_KEYS = {
   'Revenues': 'total_revenue',
   'RevenueFromContractWithCustomerExcludingAssessedTax': 'rev_from_ceat', 
}

OP_INC_KEYS = {
   'OperatingIncomeLoss': 'operating_income'
}

def calculate_period_days(start_date:str, end_date:str)-> int:
   start = datetime.strptime(start_date, '%Y-%m-%d')
   end = datetime.strptime(end_date, '%Y-%m-%d')
   difference = end - start
   return difference.days


def create_income_statements():
   for k in main_keys:
      try:
         path_units = path.get(k,{}).get('units',{})
         path_usd = path_units.get('USD',[]) ## change to dynamic currency

         if not path_usd:
            # print(f'No USD data found for {k} - {company.ticker}')
            continue
         
         sorted_path = reversed(path_usd)
         
         for json_obj in sorted_path: ## Using reversed(list) retrieves entries chronologically from most recent to oldest
            try:
               end = json_obj.get('end')
               frame = json_obj.get('frame')

               if not (frame and end):
                  continue
               
               co_inc_key = frame+"-"+end
               if co_inc_key in co_inc_dict:
                  continue

               new_inc=IncomeStatement(
                  company_cik = company.cik,
                  start = json_obj.get('start', None),
                  end =  end,
                  net_income = json_obj.get('val', None),
                  form = json_obj.get('form', None),
                  filed = json_obj.get('filed', None),
                  accn = json_obj.get('accn', None),
                  fp = json_obj.get('fp', None),
                  fy = json_obj.get('fy', None),
                  frame = frame,
                  period_days = -1
               )

               if new_inc.start and new_inc.end:
                  try:
                     new_inc.period_days = calculate_period_days(new_inc.start, new_inc.end)
                  except Exception as e:
                     new_inc.period_days = -1

               setattr(new_inc, 'key', k)
               
               co_inc_dict[co_inc_key] = new_inc
               income_statements.append(co_inc_dict[co_inc_key])
            except Exception as e:
               print(f'Error processing JSON object: {e}')
               continue
            
      except Exception as e:
         print(f"Error processing key {k} - {company.ticker}: {e}")
         continue


def set_revenues(co_inc_key: str):
   for k, db_attr in REV_KEYS.items():
      try:
         path_usd = path.get(k).get('units',{}).get('USD',[])
         if not path_usd:
            continue
         
         reversed_path = reversed(path_usd)
         for json_obj in reversed_path:
            json_frame = json_obj.get('frame', None)
            json_end = json_obj.get('end', None)
            
            if not (json_frame and json_end):
               continue
            
            json_inc_key = json_frame+"-"+json_end
            if json_inc_key != co_inc_key:
               continue
            
            inc = co_inc_dict[co_inc_key]

            if inc.total_revenue == None:
               setattr(inc, 'total_revenue', json_obj.get('val'))
            else:
               setattr(inc, db_attr, json_obj.get('val'))
            
      except Exception as e:
         # print(f'{k} - {e} - {company.ticker}')
         continue


def set_operating_income(co_inc_key: str):
   for k, db_attr in OP_INC_KEYS.items():
      try:
         path_usd = path.get(k).get('units',{}).get('USD',[])
         if not path_usd:
            continue
         
         reversed_path = reversed(path_usd)
         for json_obj in reversed_path:
            json_frame = json_obj.get('frame', None)
            json_end = json_obj.get('end', None)
            
            if not (json_frame and json_end):
               continue
            
            json_inc_key = json_frame+"-"+json_end
            if json_inc_key != co_inc_key:
               continue
            
            inc = co_inc_dict[co_inc_key]
          
            setattr(inc, db_attr, json_obj.get('val'))

      except Exception as e:
         # print(f'{k} - {e} - {company.ticker}')
         continue


def send_to_db():
   current_time = time.time()
   elapsed = current_time - start_time
   print(f'Committing {len(income_statements)} sheets to DB - {truncate_num(elapsed, 2)}s elapsed.')
   db.session.add_all(income_statements)
   db.session.commit()
   income_statements.clear()


def truncate_num(num, decimals):
   factor = 10 ** decimals
   return math.floor(num * factor) / factor

## DEFINITIONS END #####################################################################################################

if __name__ == '__main__':
   income_statements = []
   company_tracker = set()

   with app.app_context():
      print("Starting seed...")

      ## Comment these out if you don't wish to delete table before beginning #################################
      db.session.query(IncomeStatement).delete()
      db.session.commit()
      #########################################################################################################
      
      # companies = [Company.query.filter(Company.id == 2153).first()]
      companies = Company.query.all()
      # companies = Company.query.filter(Company.id <= 200).all()
      
      for company in companies:
         co_inc_dict = {}
         if company.cik not in company_tracker:
            company_tracker.add(company.cik)
            # print(company.id, company.name, company.cik)
            db.session.refresh(company)
            
            try:
               file_path = f'json/CIK{company.cik_10}.json'
               json_file = open(file_path,'r')
               data = json.load(json_file)
               
               gaap = data.get('facts',{}).get('us-gaap', {})
               ifrs = data.get('facts',{}).get('ifrs-full', {})
               
               if not gaap and not ifrs:
                  continue
               path = gaap if gaap else ifrs
               
               create_income_statements()
               for key in co_inc_dict.keys():
                  set_revenues(key)
                  set_operating_income(key)
               
               json_file.close()

            except Exception as e:
               # print(f'{company.name} - {str(e)}')
               continue
            # except json.JSONDecodeError as e:
            #    print(f'{str(e)}')
            # except IntegrityError as e:
            #    print(f'{str(e)}')
            
         if len(income_statements) > 50000:
            send_to_db()
            
      if len(income_statements) > 0:
         send_to_db()

   end_time = time.time()
   elapsed = end_time - start_time
   print(f'{truncate_num(elapsed, 2)} seconds elapsed')
   print("Seed successful")