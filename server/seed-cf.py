#!/usr/bin/env python3

from random import random, randint, choice as rc
import os
import json
import time
from app import app
from models import db, Company, CashFlowsStatement
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

with app.app_context():
   start_time = time.time()
   print("Starting seed...")

   ## Comment these out if you don't wish to delete table before beginning ##

   # db.session.query(CashFlowsStatement).delete()
   # db.session.commit()

   ##########################################################################
   
   r = randint(1,10165)
   companies = Company.query.filter(Company.id <= 10165)
   
   cf_statements = []
   cf_count = 0
   
   company_tracker = {}
   company_count = 0

   co_dates = {}
   co_dates_count = 0

   for company in companies:
      if company.cik not in company_tracker.values():
         cf_statements = {cf.frame: cf for cf in CashFlowsStatement.query.filter(CashFlowsStatement.company_cik == company.cik).all()}
         print(company.id, company.name, company.cik)
         db.session.refresh(company)
         
         file_path = f'json/CIK{company.cik_10}.json'
         json_file = open(file_path,'r')
         
         try:
            data = json.load(json_file)
            gaap = data.get('facts', {}).get('us-gaap')
            end_dates = {}
            end_count = 0
            
            def make_cf(key:str):
               global end_count, cf_count
               if x.get('frame') and x.get('end') not in end_dates.values():
                  new_cf_statement=CashFlowsStatement(
                     company_cik = company.cik,
                     start = x.get('start'),
                     end =  x.get('end'),
                     opr_cf = x.get('val'),
                     form = x.get('form'),
                     filed = x.get('filed'),
                     accn = x.get('accn'),
                     fp = x.get('fp'),
                     fy = x.get('fy'),
                     frame = x.get('frame'),
                     op_cf_key = key
                  )
                  cf_statements.append(new_cf_statement)
                  cf_count += 1
                  print(cf_count, key)

                  end_count += 1
                  end_dates[end_count] = x.get('end')


               else:
                  pass
            
            op_cf_keys = ['NetCashProvidedByUsedInOperatingActivities',
                       'NetCashProvidedByUsedInOperatingActivitiesContinuingOperations',
                     ]
            
            inv_cf_keys = ['NetCashProvidedByUsedInInvestingActivities',
                           'NetCashProvidedByUsedInInvestingActivitiesContinuingOperations',
                        ]
            
            fin_cf_keys = ['NetCashProvidedByUsedInFinancingActivities',
                           'NetCashProvidedByUsedInFinancingActivitiesContinuingOperations',
                        ]
         
            for key in op_cf_keys:
               if gaap.get(key):
                  for x in gaap.get(key, {}).get('units', {}).get('USD', None):
                     make_cf(key)
               else:
                  pass
            
            for key in inv_cf_keys:
               if gaap.get(key):
                  for x in gaap.get(key, {}).get('units', {}).get('USD', None):
                     cf_statement = cf_statements.get(x.get('frame'))
                     if cf_statement:
                        cf_statement.inv_cf = x.get('val')
                        print(cf_statement, key)
                     else:
                        pass
                        
               else:
                  pass

            for key in fin_cf_keys:
               if gaap.get(key):
                  for x in gaap.get(key, {}).get('units', {}).get('USD', None):
                     cf_statement = cf_statements.get(x.get('frame'))
                     if cf_statement:
                        cf_statement.fin_cf = x.get('val')
                        print(cf_statement, key)
                     else:
                        pass
               else:
                  pass
            
            end_dates.clear()
            end_count = 0
            company_count += 1
            company_tracker[company_count] = company.cik
            
         except json.JSONDecodeError:
            pass
         except IntegrityError:
            print(f'{company.id} - {company.name} row already deleted')
            pass
         except Exception as e:
            print(f'{str(e)}')
            pass
         
         json_file.close()
         print("JSON closed")
         
      else:
         pass
   
         if len(cf_statements) > 50000:
            db.session.add_all(cf_statements)
            db.session.commit()
            print(f'Committed previous {len(cf_statements)} entries')
            cf_statements.clear()
   db.session.commit()
   print("Netting cashflow statements")

   all_cf_statements = CashFlowsStatement.query.all()
   if all_cf_statements:
      for cf in all_cf_statements:
         if cf.opr_cf and cf.inv_cf and cf.fin_cf:
            cf.net_cf = cf.opr_cf + cf.inv_cf + cf.fin_cf
            print(cf)
         else:
            pass
   else:
      pass
   db.session.commit()
   

   if len(cf_statements)>0:
      db.session.add_all(cf_statements)
      db.session.commit()
      print(f'Committed remaining entries')
   else:
      pass

   end_time = time.time()
   elapsed = end_time - start_time
   print(f'{elapsed} seconds elapsed')
   print("Seed successful")