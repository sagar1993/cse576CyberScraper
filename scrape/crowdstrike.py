try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd


def parse_page(key, url):
    doc = {}
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    page = urllib2.urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    texts = soup.find('div', class_="entry clr").get_text().encode('utf-8').strip()
    heading = soup.find('h1').get_text()
    # print texts
    # print heading
    doc["keyword"] = key
    doc["article-url"] = url
    doc["article-name"] = heading
    doc["content"] = texts
    result.append(doc)
    df = pd.DataFrame(result)
    df.to_csv("../data/" + key + "crowdstrike.csv")
    #df.to_csv("data/" + key + "crowdstrike.csv")
    
result = []
df = pd.read_csv("crowdstrike-list.csv")
rows = df.shape[0]
for i in range(rows):
    keyword = df.key.ix[i]
    link = df.url.ix[i]
    # print(keyword+" - "+link)
    parse_page(keyword, link)
