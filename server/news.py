import feedparser as fp
import json
import time
from json import JSONDecodeError
from app import app
from models import db, Company, Article




articles = []

while True:
    start = time.time()
    print("Fetching feed.")
    url = "https://www.globenewswire.com/RssFeed/orgclass/1/feedTitle/GlobeNewswire%20-%20News%20about%20Public%20Companies"
    feed = fp.parse(url)
    with app.app_context():
        # db.session.query(Article).delete()
        # db.session.commit()

        for entry in feed.entries:
            article = Article(
                        title = entry.title,
                        source = entry.publisher,
                        source_url = entry.id,
                        companies = []
                    )
            for tag in entry.tags:
                if any(exchange.lower() in tag.term.lower() for exchange in ('Nasdaq', 'Nyse')):
                    article.companies.append(tag.term)
            
            if len(article.companies) > 0:
                article_exists = False
                for a in Article.query.all():
                    if a.source_url.lower() in article.source_url.lower():
                        article_exists = True
                        break
                if not article_exists:  # Only add if article doesn't exist
                    print(article.companies, article.title)
                    articles.append(article)
        
        if len(articles) > 0:
            db.session.add_all(articles)
            db.session.commit()
            articles.clear()
                    
    end = time.time()
    print (end - start)

    test_file = open("testfile.json", "w")
    dump = json.dump(feed, test_file, indent = 4)
    print("Fetch completed.")
    print("Waiting 15 seconds...")
    time.sleep(15)


