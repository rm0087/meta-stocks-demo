#!/usr/bin/env python3

from app import app
from models import db, IncomeStatement
from sqlalchemy import and_, func, desc
from sqlalchemy.exc import IntegrityError
import time

with app.app_context():
    start_time = time.time()

    # duplicates = db.session.query(
    #     IncomeStatement.company_cik, 
    #     IncomeStatement.end,
    #     IncomeStatement.total_revenue,
    #     func.count(IncomeStatement.id).label('count')
    # ).group_by(
    #     IncomeStatement.company_cik, 
    #     IncomeStatement.end,
    #     IncomeStatement.total_revenue,
    # ).having(func.count(IncomeStatement.id) > 1).all()

    # for duplicate in duplicates:
    #     print(f'Deleting duplicate {duplicates.index(duplicate)+1} of {len(duplicates)}')
    #     # Fetch all balance sheets that match the duplicate criteria
    #     sheets = IncomeStatement.query.filter_by(
    #         company_cik=duplicate.company_cik,
    #         end=duplicate.end,
    #         total_revenue = duplicate.total_revenue
    #     ).order_by(IncomeStatement.id).all()

    #     # Keep the first one and delete the rest
    #     for sheet in sheets[1:]:  # Keep the first (index 0), delete others
    #         db.session.delete(sheet)

    # # Commit the transaction to apply deletions
    # db.session.commit()

#################################################################################################################################################################################################################################

    duplicates = db.session.query(
        IncomeStatement.company_cik, 
        IncomeStatement.end,
    
        func.count(IncomeStatement.id).label('count')
    ).group_by(
        IncomeStatement.company_cik, 
        IncomeStatement.end,
    ).having(func.count(IncomeStatement.id) > 1).all()

    for duplicate in duplicates:
        
        # Fetch all balance sheets that match the duplicate criteria
        sheets = IncomeStatement.query.filter_by(
            company_cik=duplicate.company_cik,
            end=duplicate.end,
        ).order_by(desc(IncomeStatement.total_revenue)).all()

        # Keep the first one and delete the rest
        for sheet in sheets[1:]:  # Keep the first (index 0), delete others
            db.session.delete(sheet)
            print(f'Deleted duplicate {duplicates.index(duplicate)+1} of {len(duplicates)}')

    # Commit the transaction to apply deletions
    db.session.commit()
    end_time = time.time()
    elapsed = end_time - start_time
    print(f'{elapsed} seconds elapsed.')
    print('Deletion commited.')