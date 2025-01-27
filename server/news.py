import feedparser as fp
import json
from datetime import datetime, timedelta
import time
from json import JSONDecodeError
from app import app
from models import db, Company, Article

articles = []

def get_time(time:list):
    try:
        year = time[0]
        month = time[1]
        day = time[2]
        hour = time[3]
        minute = time[4]
        second = time[5]
        return datetime(year, month, day, hour, minute, second) - timedelta(hours=5)
    except IndexError:
        print("Index out of range")
        return datetime(0, 0, 0, 0, 0, 0)

while True:
    start = time.time()
    curr_time = time.strftime("%H:%M:%S", time.localtime())
    print(f"({curr_time}) Fetching GlobeNewsWire...")
    url = "https://www.globenewswire.com/RssFeed/orgclass/1/feedTitle/GlobeNewswire%20-%20News%20about%20Public%20Companies"
    feed = fp.parse(url)
    
    with app.app_context():
    
        # db.session.query(Article).delete()
        # db.session.commit()

        for entry in feed.entries:
            article = Article()
            
            try:
                article.title = entry.title
                article.source = entry.publisher
                article.source_url = entry.id
                article.companies = []
                article.date_time = get_time(entry.published_parsed)
                if entry.updated_parsed:
                    article.update_time = get_time(entry.updated_parsed)
            except AttributeError:
                print("Attribute Error")
                pass
            
            for tag in entry.tags:
                if any(exchange.lower() in tag.term.lower() for exchange in ('Nasdaq', 'Nyse')):
                    try:
                        article.companies.append(tag.term.split(':', 1)[1])
                    except IndexError:
                        article.companies.append(tag.term)
                
            if len(article.companies) > 0:
                article_exists = False
                for a in Article.query.all():
                    if a.source_url.lower() in article.source_url.lower():
                        article_exists = True
                        break
                if not article_exists:  # Only add if article doesn't exist
                    print(article.date_time, article.companies, article.title)
                    articles.append(article)
        
        if len(articles) > 0:
            db.session.add_all(articles)
            db.session.commit()
            articles.clear()
                    
    end = time.time()
    # print (end - start)
    test_file = open("testfile.json", "w")
    dump = json.dump(feed, test_file, indent = 4)
    time.sleep(15)


    # ## FIX COMPANY NAMES
    # for article in Article.query.all():
    #     article.companies = [company.split(':', 1)[1] for company in article.companies]
    #     db.session.add(article)
    #     db.session.commit()
    # db.session.commit()
        


