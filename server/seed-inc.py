#!/usr/bin/env python3

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
main_keys = ['NetIncomeLoss',
             'NetIncomeLossAvailableToCommonStockholdersBasic',
             'ComprehensiveIncomeAttributableToOwnersOfParent',
            ]

all_keys =  [  'Revenues',
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

ALL_KEYS = {
      'Revenues': 'total_revenue',
   }

def calculate_period_days(start_date:str, end_date:str)-> int:
   start = datetime.strptime(start_date, '%Y-%m-%d')
   end = datetime.strptime(end_date, '%Y-%m-%d')
   difference = end - start
   return difference.days


def create_income_statements(path):
   for k in main_keys:
      try:
         path_units = path.get(k).get('units')
         path_usd = path_units.get('USD')
         if path_units and path_usd:
            for json_obj in path_usd:
                  accn = json_obj.get('accn')
                  frame = json_obj.get('frame')
                  if frame and accn:
                     new_inc=IncomeStatement(
                        company_cik = company.cik,
                        start = json_obj.get('start'),
                        end =  json_obj.get('end'),
                        net_income = json_obj.get('val'),
                        form = json_obj.get('form'),
                        filed = json_obj.get('filed'),
                        accn = json_obj.get('accn'),
                        fp = json_obj.get('fp'),
                        fy = json_obj.get('fy'),
                        frame = json_obj.get('frame'),
                     )
                     new_inc.period_days = calculate_period_days(new_inc.start, new_inc.end)
                     setattr(new_inc, 'key', k)
                     co_inc_dict[frame+'-'+accn] = new_inc
                     income_statements.append(new_inc)
      except Exception as e:
         # print(e)
         pass
               

def set_revenues(path):
   for inc in co_inc_dict.values():
      frame = inc.frame
      accn = inc.accn
      for k, db_attr in ALL_KEYS.items():
         path_usd = path.get(k).get('units').get('USD')
         if path_usd:
            for json_obj in path_usd:
               if json_obj.get('frame') == frame and json_obj.get('accn') == accn:
                  setattr(inc, db_attr, json_obj.get('val'))

def send_to_db():
   print(f'Committing {len(income_statements)} sheets to DB')
   db.session.add_all(income_statements)
   db.session.commit()
   income_statements.clear()

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
      
      # companies = [Company.query.filter(Company.id == 19).first()]
      # companies = Company.query.all()
      companies = Company.query.filter(Company.id <= 200).all()
      
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
               gaap = data.get('facts', {}).get('us-gaap')
               ifrs = data.get('facts', {}).get('ifrs-full')
               path = ''
               
               if gaap:
                  path = gaap
               else:
                  path = ifrs

               create_income_statements(path)
               # set_revenues(path)
               
               json_file.close()

            except Exception as e:
               print(f'{company.name} - {str(e)}')
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
      print(f'{elapsed} seconds elapsed')
      print("Seed successful")