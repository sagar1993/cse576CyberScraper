try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time


def parse_page(key, url):
    driver.maximize_window()
    driver.get(url)
    # time.sleep(5)
    doc = {}
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, 'html.parser')
    if '/connect/' in url:
        texts = soup.find('div', class_="content-wrapper").get_text().encode('utf-8').strip()
        heading = soup.find('h1').get_text().encode('utf-8').strip()
        print(heading)
    else:
        texts = soup.find('div', class_="blog-post__content").get_text().encode('utf-8').strip()
        heading = soup.find('h1').get_text().encode('utf-8').strip()
        print(heading)
    doc["keyword"] = key
    doc["article-url"] = url
    doc["article-name"] = heading
    doc["content"] = texts
    result.append(doc)
    df = pd.DataFrame(result)
    df.to_csv("../data/" + key + "symantec.csv")
    # df.to_csv("data/" + key + "symantec.csv")


driver = webdriver.Chrome()
result = []
df = pd.read_csv("symantec-list.csv")
rows = df.shape[0]
for i in range(rows):
    keyword = df.key.ix[i]
    link = df.url.ix[i]
    if i==0:
        parse_page(keyword, link)
    else:
        if keyword == df.key.ix[i-1]:
            parse_page(keyword, link)
        else:
            result = []
            parse_page(keyword, link)
    
