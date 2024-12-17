import time
import random
import os
import requests
import json
import re
from dotenv import load_dotenv
# Flask
from app import app
from models import Company
# Keyword Parsing
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

load_dotenv()

proxies = {
    'http': os.getenv('PROXY_2'),
    'https': os.getenv('PROXY_2')
}

headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'
            }

def get_sec_filing(filing_url):
    r = requests.get(filing_url, headers=headers, proxies=proxies)
    print(r.status_code)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup.get_text()

def clean_text(text):
    stop_words = set(stopwords.words('english'))
    words = [word for word in text.split() if word.isalnum() and word.lower() not in stop_words]
    return ' '.join(words)

def extract_keywords(text, n=10):
    global vectorizor
    vectorizer1 = TfidfVectorizer(max_features=n,
                                  ngram_range=(1, 3),  # Unigrams, bigrams, trigrams
                                    max_df=0.85,         # Ignore overly common terms
                                    min_df=2,            # Ignore rare terms
                                    stop_words='english',
                                    sublinear_tf=True)
    vectorizor = vectorizer1
    tfidf_matrix = vectorizer1.fit_transform([text])
    keywords = vectorizer1.get_feature_names_out()
    return keywords

url = 'https://www.ibisworld.com/us/company/apple-inc/405800/'

text = get_sec_filing(url)
cleaned_text = clean_text(text)

vectorizor = ""
keywords = extract_keywords(cleaned_text, n=1000)

print(keywords)














# def clean_markup(text):
#     # Remove patterns like "0 2px", "1pt", "solid", etc.
#     text = re.sub(r'(\b\d+px|\b\d+pt|\bsolid\b|\bdouble\b)', '', text)
    
#     # Remove excessive whitespace created by the previous step
#     text = re.sub(r'\s+', ' ', text).strip()
    
#     return text

# with app.app_context():

# r = requests.get(f"https://www.sec.gov/Archives/edgar/data/320193/000032019324000081/0000320193-24-000081.txt", 
#                  headers=headers,
#                  proxies = proxies
#                  )
    




