#!/usr/bin/env python3

from random import randint
import os
import json
import time
from app import app
from models import db, Company, BalanceSheet
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

with app.app_context():
   start_time = time.time()
   print("Starting seed...")

   ## Comment these out if you don't wish to delete table before beginning ##

   db.session.query(BalanceSheet).delete()
   db.session.commit()

   ##########################################################################
   
   r = randint(1,10165)
   companies = Company.query.filter(Company.id <= 10165)
   
   all_bs = []
   bs_count = 0
   
   company_tracker = {}
   company_count = 0
            
   main_keys = ['Assets',]

   all_keys = ['AssetsCurrent',
               'AssetsNoncurrent',
               'Liabilities',
               'LiabilitiesCurrent',
               'LiabilitiesNoncurrent',
               'StockholdersEquity',
               'LiabilitiesAndStockholdersEquity',
               'StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest',
               'Goodwill',
               'Cash', 
               'CashAndCashEquivalentsAtCarryingValue', 
               'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents',
               'IntangibleAssetsNetExcludingGoodwill'
               ]
   
   def make_bs(key:str, x):
               global end_count, bs_count
               if x.get('frame') and x.get('end') not in end_dates.values():
                  new_bs=BalanceSheet(
                     company_cik = company.cik,
                     start = x.get('start'),
                     end =  x.get('end'),
                     total_assets = x.get('val'),
                     form = x.get('form'),
                     filed = x.get('filed'),
                     accn = x.get('accn'),
                     fp = x.get('fp'),
                     fy = x.get('fy'),
                     frame = x.get('frame'),
                  )
                  all_bs.append(new_bs)
                  bs_count += 1
                  print(bs_count, key)

                  end_count += 1
                  end_dates[end_count] = x.get('end')
               else:
                  pass

   def amend_bs(key:str, bs):
      if key == 'AssetsCurrent':
         bs.assets_current = x.get('val')
      if key == 'AssetsNoncurrent':
         bs.assets_noncurrent = x.get('val')
      if key == 'Liabilities':
         bs.total_liabilities = x.get('val')
      if key == 'LiabilitiesCurrent':
         bs.liabilities_current = x.get('val')
      if key == 'LiabilitiesNoncurrent':
         bs.liabilities_noncurrent = x.get('val')
      if key == 'StockholdersEquity':
         bs.total_stockholders_equity = x.get('val')
      if key == 'LiabilitiesAndStockholdersEquity':
         bs.total_liabilities_and_stockholders_equity = x.get('val')
      if key == 'StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest':
         bs.total_stockholders_equity_nci = x.get('val')
      if key == 'Goodwill':
         bs.goodwill = x.get('val')
      if key == 'Cash':
         bs.cash = x.get('val')
      if key == 'CashAndCashEquivalentsAtCarryingValue':
         bs.cash_and_equiv = x.get('val')
      if key == 'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents':
         bs.cash_all = x.get('val')
      if key == 'IntangibleAssetsNetExcludingGoodwill':
         bs.intangible_assets = x.get('val')
      print(bs, key)

   for company in companies:
      
      if company.cik not in company_tracker.values():
         
         print(company.id, company.name, company.cik)
         db.session.refresh(company)
         
         file_path = f'json/CIK{company.cik_10}.json'
         json_file = open(file_path,'r')
         
         try:
            data = json.load(json_file)
            gaap = data.get('facts', {}).get('us-gaap')
            end_dates = {}
            end_count = 0
            
            for key in main_keys:
               if gaap.get(key):
                  for x in gaap.get(key, {}).get('units', {}).get('USD', None):
                     make_bs(key, x)
               else:
                  pass

            co_bs_dict = {bs.frame: bs for bs in all_bs if bs.company_cik == company.cik}
               
            for key in all_keys:
               if gaap.get(key):
                  for x in gaap.get(key, {}).get('units', {}).get('USD', None):
                     bs = co_bs_dict.get(x.get('frame'))
                     if bs:
                        amend_bs(key, bs)
                     else:
                        pass
            
            no_l = [bs for bs in co_bs_dict.values() if bs.total_liabilities == None]
            no_tse = [bs for bs in co_bs_dict.values() if bs.total_stockholders_equity == None]
            no_ce = [bs for bs in co_bs_dict.values() if bs.cash_and_equiv == None]
            
            for bs in no_l:
               lc = bs.liabilities_current
               lnc = bs.liabilities_noncurrent
               tse = bs.total_stockholders_equity
               a = bs.total_assets
               tlse = bs.total_liabilities_and_stockholders_equity
               tse_nci = bs.total_stockholders_equity_nci

               if lc and lnc:
                  bs.total_liabilities = lc + lnc
                  print(f'{bs} added total_liabilities')
               elif a and tse: 
                  bs.total_liabilities = a - tse
                  print(f'{bs} added total_liabilities')
               elif tlse and tse_nci:
                  bs.total_liabilities = tlse - tse_nci
                  print(f'{bs} added total_liabilities')
               else:
                  pass
            
            for bs in no_tse:
               tlse = bs.total_liabilities_and_stockholders_equity
               l = bs.total_liabilities
               tse_nci = bs.total_stockholders_equity_nci
               
               if l and tlse:
                  bs.total_stockholders_equity = tlse - l
                  print(f'{bs} added total_stockholders_equity')
               elif tse_nci:
                  bs.total_stockholders_equity = tse_nci
                  print(f'{bs} added total_stockholders_equity')
               else:
                  pass

            for bs in no_ce:
               c = bs.cash
               ca = bs.cash_all

               if c:
                  bs.cash_and_equiv = c
                  print(f'{bs} added cash_and_equiv')
               elif ca:
                  bs.cash_and_equiv = ca
                  print(f'{bs} added cash_and_equiv')
               else:
                  pass       
            
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
   
      if len(all_bs) > 50000:
         print(f'Committing {len(all_bs)} sheets to DB')
         db.session.add_all(all_bs)
         db.session.commit()
         print(f'Committed {len(all_bs)} sheets to DB')
         all_bs.clear()
      else:
         pass
      
      company_count += 1
      company_tracker[company_count] = company.cik
      
   print("Committing remaining balance sheets...")
   if len(all_bs) > 0:
      db.session.add_all(all_bs)
      db.session.commit()
      print(f'Committed all new balance sheets to DB')
   
   end_time = time.time()
   elapsed = end_time - start_time
   print(f'{elapsed} seconds elapsed')
   print("Seed successful")

  

   