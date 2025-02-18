#!/usr/bin/env python3
import time
from datetime import datetime as dt
from random import randint
import os
import json
from app import app
from models import db, Company, IncomeStatement
from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError

## FUNCTIONS BEGIN #####################################################################################################
def is_date_in_range(start_date:str, end_date:str, check_date:str) -> bool:
   start = dt.strptime(start_date, "%Y-%m-%d")
   end = dt.strptime(end_date, "%Y-%m-%d")
   check = dt.strptime(check_date, "%Y-%m-%d")

   start, end = min(start, end), max(start, end)

   return start <= check <= end

## FUNCTIONS END #####################################################################################################
if __name__ == '__main__':
   start_time = time.time()
   income_statements = []
   inc_count = 0
   company_tracker = {}
   company_count = 0

   with app.app_context():
      print("Starting income statement data normalization...")
      ciks = db.session.execute(select(Company.cik)).first()
      for cik in ciks:
         incs = IncomeStatement.query.filter(IncomeStatement.company_cik == cik).all()
         incs_10ks = [inc for inc in incs if inc.form == "10-K"]
         incs_10qs = [inc for inc in incs if inc.form == "10-Q"]
         print(len(incs_10ks))
         print(len(incs_10qs))
         # for inc_10k in incs_10ks:

      ## for each cik:
         ## gather all income statements with matching cik
         ## find all 10-K filings
         ## for each 10-k filing:
            ## check which 10-Q's fall into date range of 10-K
            ## check if there are THREE 10-Q's that are in this range
            ## if there are THREE 10-Q's: 
               ## for the 10-Q's in range:
                  ## subtract all 10-Q figures from corresponding 10-K figures
                  ## create income statement entry with newly derived Q4 data    
            ## else if there are NOT THREE 10-Q's:
               ## do nothing (for now)
      







   end_time = time.time()
   elapsed = end_time - start_time
   print(f'{elapsed} seconds elapsed')
   print("Seed successful")