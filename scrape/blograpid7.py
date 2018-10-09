# this script uses a search engine to parse blograpid7, please install selenium driver

import urllib2
import re
from bs4 import BeautifulSoup
import json
import datetime
from dateutil.parser import parse
from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd

import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random

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

    # chooses between multiple search engines to reduce counterscraping risk
    searchChoice = random.randint(1, 1)
    chromedriver = os.getcwd()+'/chromedriver'
    os.environ["webdriver.chrome.driver"] = chromedriver
    browser = webdriver.Chrome(chromedriver)

    result = []
    if searchChoice == 1:
        
        url = 'https://google.com/search?q=' + query + '+site:https://blog.rapid7.com/'
        page = urllib2.urlopen(url)
        browser.get(url)
        soup = BeautifulSoup(browser.page_source,"lxml")
        name_link = soup.find_all('h3', class_='r') #names of titles
        link = soup.find_all('cite') # links
        for n_link, l in zip(name_link,link):

            # for each link result
            d = {}
            html = urllib2.urlopen(l).read()
            d["query"] = query
            d["url"] = l
            d["text"] = text_from_html(html).encode('utf-8').strip()
            result.append(d)
            # print(f'{n_link.text}\n{l.text}')

    df = pd.DataFrame(result)
    df.to_csv(query+"securelist.csv")
