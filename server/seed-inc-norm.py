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

def create_q4_db_entry(q4_rev_sum, q4_inc_sum, end_date, cik):
   new_q4 = IncomeStatement(total_revenue = q4_rev_sum, net_income = q4_inc_sum, end = end_date, company_cik = cik)
   db.session.add(new_q4)
   db.session.commit()

## FUNCTIONS END #####################################################################################################
if __name__ == '__main__':
   start_time = time.time()
   errors = set()
   with app.app_context():
      print("Starting income statement data normalization...")
      ciks = db.session.execute(select(Company.cik)).scalars().all()
      # incs = IncomeStatement.query.all()
      for cik in ciks:
         print(cik)
         cik_incs = IncomeStatement.query.filter(IncomeStatement.company_cik == cik).all()
         incs_10ks = [inc for inc in cik_incs if inc.period_days >= 320]
         incs_10qs = [inc for inc in cik_incs if inc.period_days <= 110]
         for inc_10k in incs_10ks:
            try:
               period_filings = [inc_10k]
               for inc_10q in incs_10qs:
                  if is_date_in_range(inc_10k.start, inc_10k.end, inc_10q.end):
                     period_filings.append(inc_10q)
                  if len(period_filings) == 4:
                     rev_sum = period_filings[1].total_revenue + period_filings[2].total_revenue + period_filings[3].total_revenue
                     q4_rev_sum = period_filings[0].total_revenue - rev_sum

                     inc_sum = period_filings[1].net_income + period_filings[2].net_income + period_filings[3].net_income
                     q4_inc_sum = period_filings[0].net_income - inc_sum
                     create_q4_db_entry(q4_rev_sum, q4_inc_sum, period_filings[0].end, cik)
                     break
            except TypeError as e:
               print(cik, f' - {e}')
               errors.add(cik)
               pass


      ## for each cik:
         ## gather all income statements with matching cik
         ## find all 300+ day filings
         ## for each 300+ day filings
            ## check which 90ish day reports fall into date range of 300+ day
            ## check if there are THREE 90ish day reports that are in this range
            ## if there are THREE 90ish day reports: 
               ## for the 90ish day reports in range:
                  ## subtract all 90ish day reportsigures from corresponding 300+ day figures
                  ## create income statement entry with newly derived Q4 data    
            ## else if there are NOT THREE 90ish day reports:
               ## do nothing (for now)
      







   end_time = time.time()
   elapsed = end_time - start_time
   print(f'{elapsed} seconds elapsed')
   print("Seed successful")
   print("Errors:", errors)