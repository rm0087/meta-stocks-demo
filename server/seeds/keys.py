#!/usr/bin/env python3

from random import randint
from app import app
from models import db, Company
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
import os
import json
import time

with app.app_context():
   
   start_time = time.time()
   print("Starting seed...")

   max = 10165
   r = randint(1,max)
   companies = Company.query.filter(Company.id <= max)
 
   company_tracker = {}
   company_count = 0

   key_tracker = set()
   currencies = set()
   currency_dict = {}

   for company in companies:
      if company.cik not in company_tracker.values():
         print(company.id, company.name, company.cik)
         db.session.refresh(company)
         
         file_path = f'json/CIK{company.cik_10}.json'
         json_file = open(file_path,'r')
         
         try:
            data = json.load(json_file)
            
            gaap = data.get('facts', {}).get('us-gaap')
            ifrs = data.get('facts', {}).get('ifrs-full')
            
            end_dates = {}
            end_count = 0
            
            def accounting(path):
               for x in path:
                  key_tracker.add(f"'{x}'")
                  # print(x)
                  for key, value in path.get(x).get('units').items():
                     if len(key) == 3 and key == key.upper():
                        currencies.add(key)
                        
                        if key in currency_dict:
                           currency_dict[key] += 1
                        else:
                           currency_dict[key] = 1
                     print(key)

            
            accounting(gaap if gaap else ifrs)

              
         except json.JSONDecodeError:
            # Company.query.filter(Company.cik == company.cik).delete()
            # db.session.commit()
            # print(f'{company.id} - {company.name} deleted from company DB.')
            print(f'JSON decode error. Closing JSON file for company {company.cik} - {company.name} - {company.ticker}')
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

      company_count += 1
      company_tracker[company_count] = company.cik
   
   key_tracker_final = sorted(key_tracker)
   currencies_final = sorted(currencies)

   with open('keys.txt', 'w') as file1:
      file1.write(",\n".join(key_tracker_final))
   file1.close()

   with open('currencies.txt', 'w') as file2:
      file2.write(",\n".join(currencies_final))
   file2.close()

   with open('currency_count.txt', 'w') as file3:
      test = []
      for key, value in currency_dict.items():
         file3.write((f"{key} : {value}\n"))
   file3.close()
   print(currency_dict)
   print(f'{len(key_tracker_final)} keys written to {file1.name}')
   print(f'{len(currencies_final)} keys written to {file2.name}')
   end_time = time.time()
   elapsed = end_time - start_time
   print(f'{elapsed} seconds elapsed')