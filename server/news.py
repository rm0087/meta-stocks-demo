import feedparser as fp
import json
from datetime import datetime
import time
from json import JSONDecodeError
from app import app
from models import db, Company, Article

articles = []

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
            try:
                year = entry.published_parsed[0]
                month = entry.published_parsed[1]
                day = entry.published_parsed[2]
                hour = entry.published_parsed[3]
                minute = entry.published_parsed[4]
                second = entry.published_parsed[5]
                published = datetime(year, month, day, hour, minute, second)
                str_time = f"({hour:02d}:{minute:02d}:{second:02d})"
            except IndexError:
                published = datetime(0, 0, 0, 0, 0, 0)
                str_time = "Time error"
                print("Index out of range")
                pass

            article = Article(
                        title = entry.title,
                        source = entry.publisher,
                        source_url = entry.id,
                        companies = [],
                        date_time = published
                    )
            
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
                    print("Published:", str_time, article.companies, article.title)
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
        


