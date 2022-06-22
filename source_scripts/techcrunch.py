import re
import requests
import sys 
import os
from common_scripts import *
from datetime import datetime
from bs4 import BeautifulSoup


sys.path.append(os.path.abspath("..\labeling"))
from labeling import *

sys.path.append(os.path.abspath("..\\boto3"))
from split_db_sources import *

url = 'http://feeds.feedburner.com/Techcrunch'

def main_techcrunch(data_set,today,filename,database):

    seen =set()
    soup = get_content(url,None)
    all_items = soup.find_all('item')
   
    all_articles = []
    article = {}
    for idx in range(len(all_items)):
        
        article['title'] = cleanhtml(all_items[idx].find('title').get_text())
        article['link'] = all_items[idx].find('link').get_text()
        pubDate = all_items[idx].find('pubDate').get_text()[:-6]
        pubDate = datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S')
        pubDate = pubDate.strftime("%m/%d/%Y %H:%M:%S")
        article['pubDate'] = pubDate
        article['description'] = cleanhtml(all_items[idx].find('description').get_text())
        # techcrunch descriptions get extracted with html tags - using regex to remove tags
        # CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});') 
        # article['description']=re.sub(CLEANR, '', article['description'])
        article['source'] = 'Techcruch'
        
        all_articles.append(article)
        article = {}

    with open(database, "a", encoding='utf8') as rf:
        now = datetime.now()
        timenow = now.strftime("%m/%d/%Y %H:%M:%S")
    
        with open(filename, 'a', encoding='utf8') as wf2:
            for i,article in enumerate(all_articles):
                if str(article['link']) not in data_set and str(article['link']) not in seen   : 
                    seen.add(str(article['link']))
                    article = label_creator(article)
                    nkw = '(No Keywords detect)'
                    if article['label_for_article_name'] == nkw and article['label_description'] == nkw:
                        pass
                    else:
                        arti = timenow+ ','+ article['pubDate'] + ',' +article['source'] +','+article['title']+","+ str(article['link']) + \
                        ',' + article['description'] + ',' + article['label_for_article_name']  + ',' + article['label_description']  + ',' \
                        + article['Possible_ER_from_Article_Name'] +','+ article["possible_ER_from_Comprehend"]
                        rf.write(arti+'\n')
                        if 'IPOs' in article['label_for_article_name']  or 'Bankruptcy' in article['label_for_article_name']:
                            create_file_bankruptcy_IPO(today_date, arti)
                        split_sources(arti)
                        wf2.write(timenow + ',' + article['pubDate'] + ',' +str(article['link'])+'\n') 
                        print(str(i)+ " "+arti[40:60]+'\n')
