import requests
import os
from dotenv import load_dotenv

load_dotenv()




def get_news():
    news_key = os.getenv('NEWS_API')
        
    proxies = {
        'http':os.getenv('PROXY_2')
    }

    headers = {
        'Accept': 'content/json',
        'Content-Type': 'content/json',
        'x-api-key':news_key
    }

    try:
        r = requests.get(f'https://newsapi.org/v2/top-headlines?country=us&pageSize=100&category=business', proxies=proxies, headers=headers)
        
        if not r.ok:
            # print(r.status_code)
            print({
                'statusCode': r.status_code,
                'error': r.json()['code'],
                'details': r.json()['message']
            })

        print(r.json()['articles'])
    except Exception as e:
        print(str(e))

get_news()
