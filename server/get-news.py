import requests
import os
from dotenv import load_dotenv

load_dotenv()

proxies = {
        'http':os.getenv('PROXY_2'),
        'https':os.getenv('PROXY_2')
    }

def get_news():
    news_key = os.getenv('NEWS_API')
        
    

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


def get_x_trends():
    # X_EMAIL
    # X_PW
    # X_API_CONSUMER_KEY
    # X_API_CONSUMER_SECRET
    # X_AUTH_BEARER_TOKEN
    # X_AUTH_ACCESS_TOKEN
    # X_AUTH_SECRET
    # X_OA2_CLIENT_ID
    # X_OA2_CLIENT_SECRET
    
    bearer_token = os.getenv('X_AUTH_BEARER_TOKEN')

    headers = {
        'Authorization': 'Bearer ' + bearer_token
    }

    try:
        r = requests.get(f'https://api.x.com/1.1/statuses/user_timeline.json?screen_name=twitterapi&count=2', proxies=proxies, headers=headers)
        
        if not r.ok:
            print("Code: ", r.status_code)
            print(r.json())
            # print({
            #     'statusCode': r.status_code,
            #     'error': r.json()['code'],
            #     'details': r.json()['message']
            # })

        print(r.json())

    except Exception as e:
        print(str(e))
get_x_trends()