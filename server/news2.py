import feedparser as fp
import json
import time
from datetime import datetime
from app import app
from models import db, Company, Article

articles = []

while True:
    
    start = time.time()
    curr_time = time.strftime("%H:%M:%S", time.localtime())
    print(f"({curr_time}) Fetching PRNEWSWIRE...")
    url = "https://www.prnewswire.com/apac/rss/news-releases-list.rss"
    feed = fp.parse(url)
    
    with app.app_context():
        companies = Company.query.all()
        # db.session.query(Article).delete()
        # db.session.commit()

        for entry in feed.entries:
            year = entry.published_parsed[0]
            month = entry.published_parsed[1]
            day = entry.published_parsed[2]
            hour = entry.published_parsed[3]
            minute = entry.published_parsed[4]
            second = entry.published_parsed[5]
            published = datetime(year, month, day, hour, minute, second)
            str_time = f"({hour:02d}:{minute:02d}:{second:02d})"
            
            article = Article(
                        title = entry.title,
                        source = entry.publisher,
                        source_url = entry.id,
                        companies = [],
                        date_time = published
                    )
            for con in entry.contributors:
                for co in companies:
                    if con.name.lower() in co.name.lower():
                        article.companies.append(co.ticker)
                
            if len(article.companies) > 0:
                article_exists = False
                for a in Article.query.all():
                    if a.source_url.lower() in article.source_url.lower():
                        article_exists = True
                        break
                if not article_exists:  # Only add if article doesn't exist
                    print(str_time, article.companies, article.title)
                    articles.append(article)
        
        if len(articles) > 0:
            db.session.add_all(articles)
            db.session.commit()
            articles.clear()
                    
    # end = time.time()
    # print(end - start)
    test_file = open("testfile.json", "w")
    dump = json.dump(feed, test_file, indent = 4)
    time.sleep(15)