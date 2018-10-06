import urllib2
import re
from bs4 import BeautifulSoup
import json
import datetime
from dateutil.parser import parse
from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def parse_data_save(query):
    url = 'https://securelist.com/?s=%s' % query 
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    content = soup.find('div', class_="site-content")
    articles = content.findChildren('article')


    result = []
    for article in articles:
        url = article.find('h3', class_="entry-title").find('a').get("href")
        print(url)
        d = {}
        html = urllib2.urlopen(url).read()
        d["query"] = query
        d["url"] = url
        d["text"] = text_from_html(html).encode('utf-8').strip()
        result.append(d)
    df = pd.DataFrame(result)
    df.to_csv(query+"securelist.csv")
