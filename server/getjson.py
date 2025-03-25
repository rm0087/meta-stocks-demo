import concurrent.futures
import os
import random
import time
import requests
# from tqdm import tqdm  # Optional: for progress tracking
from models import db, Company
from app import app

def download_company_data(company, headers, total_companies):
    """Download SEC data for a single company"""
    try:
        print(f'{company.id}/{total_companies}')
        
        r = requests.get(
            f"https://data.sec.gov/api/xbrl/companyfacts/CIK{company.cik_10}.json",
            headers=headers
        )
        
        if r.status_code == 200:
            full_path = os.path.join('json', f'CIK{company.cik_10}.json')
            with open(full_path, 'wb') as f:
                f.write(r.content)
            return (company.id, True)
        else:
            print(f"Failed to download CIK{company.cik_10}: Status {r.status_code}")
            return (company.id, False)
            
    except Exception as e:
        print(f"Error processing CIK{company.cik_10}: {str(e)}")
        return (company.id, False)

def download_all_companies_concurrent(max_workers=5):
    """Download SEC data for all companies concurrently"""
    company_tracker = {}
    
    with app.app_context():
        # Ensure json directory exists
        os.makedirs('json', exist_ok=True)
        
        companies = Company.query.all()
        total_companies = len(companies)
        
        # Filter companies that haven't been processed yet
        companies_to_process = []
        for company in companies:
            if company.cik not in company_tracker.values():
                companies_to_process.append(company)
        
        print(f"Processing {len(companies_to_process)} out of {total_companies} companies")
        
        # Set up rate limiting parameters
        # SEC API has rate limits, typical limit is ~10 requests per second
        max_workers = min(max_workers, 10)  # Adjust based on SEC's rate limits
        
        # Use ThreadPoolExecutor for concurrent downloads
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Prepare the tasks
            futures = []
            for company in companies_to_process:
                # Add a small delay between submissions to avoid flooding
                time.sleep(random.uniform(0.1, 0.2))
                future = executor.submit(
                    download_company_data, 
                    company, 
                    headers, 
                    total_companies
                )
                futures.append(future)
            
            # Process results as they complete
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                company_id, success = future.result()
                if success:
                    company_tracker[len(company_tracker) + 1] = companies_to_process[i].cik
                
                # Optional: Add delay between completions to manage rate
                time.sleep(random.uniform(0.1, 0.3))
        
        print(f"Completed downloading data for {len(company_tracker)} companies")
        return company_tracker


if __name__ == "__main__":
    headers = {
        'User-Agent': 'Your Company Name yourname@example.com',
    }
    
    # Run the concurrent download with 5 workers (adjust as needed)
    company_tracker = download_all_companies_concurrent(max_workers=9)




    # count = 1
    # for key in main_keys:
    #     year = 2008
    #     while year <= 2024:
    #         q = 1
    #         while q <= 4:
    #             # print(f'https://data.sec.gov/api/xbrl/frames/us-gaap/{key}/USD/CY{year}Q{q}.json')
    #             r = requests.get(url=f'https://data.sec.gov/api/xbrl/frames/us-gaap/{key}/USD/CY{year}Q{q}.json', headers=headers)
    #             print(count, key, year, f'q{q}')
    #             print("    Status code:", r.status_code, r.reason)
    #             # print(r.content)
    #             full_path = os.path.join('acct-jsons', f'{key}-CY{year}Q{q}I.json')
    #             with open(full_path, 'wb') as f:
    #                 f.write(r.content)
    #                 f.close()
                
                
    #             q += 1
    #             count += 1

    #             time.sleep(random.uniform(1.1, 2.3))
    #         year += 1


