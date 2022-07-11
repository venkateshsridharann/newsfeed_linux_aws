import re
import os
import sys
import time 
import requests
from lxml import html
from common_scripts import *
from datetime import datetime
from bs4 import BeautifulSoup

sys.path.append(os.path.abspath("..\labeling"))
from labeling import *

url = 'http://www.finsmes.com/feed'

sys.path.append(os.path.abspath("..\\boto3"))
from split_db_sources import *

def main_FinSME(data_set,today_date,filename,database,batch):
    seen = set()
    soup = get_content(url,None)
    # print(soup)
    all_items = soup.find_all('item')
    # print(all_items)
    all_articles = []
    article = {}

    
    for idx in range(len(all_items)):
        
        article['title'] = cleanhtml(all_items[idx].find('title').get_text())
        article['link'] = all_items[idx].find('link').get_text()
        pubDate = all_items[idx].find('pubDate').get_text()[:-6]
        pubDate = datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S')
        pubDate = pubDate.strftime("%m/%d/%Y %H:%M:%S")
        article['pubDate'] = pubDate
        description = all_items[idx].find('description')
        article['source'] = 'FinSME'
        article['batch'] = batch
        article['description']  = cleanhtml(description.get_text())
        article['description'].replace(article['title'],"").replace("article['source']","")
        article['description'] = article['description'].strip()
        all_articles.append(article)
        article = {}
    
    if not os.path.isfile(database):
        file = open(database, 'w')
        file.write("Date_Collected,Date_Published,Source,Article_Name,Article_Link,Description,Keyword_label_article_name,Keyword_label_description,ER_Spacy,ML_label_Article_Name,Batch\n")
        file.close()  
    
    with open(database, "a", encoding='utf8') as rf:
        
        now = datetime.now()
        timenow = now.strftime("%m/%d/%Y %H:%M:%S")

        with open(filename, 'a', encoding='utf8') as wf2:
            for i,article in enumerate(all_articles):
                if str(article['link']) not in data_set and str(article['link']):
                    article = label_creator(article)
                    nkw = '(No Keywords detect)'
                    if article['label_for_article_name'] == nkw and article['label_description'] == nkw:
                        pass
                    else:
                        arti = timenow+ ','+ article['pubDate'] + ',' +article['source'] +','+article['title']+","+ str(article['link']) + \
                        ',' + article['description'] + ',' + article['label_for_article_name']  + ',' + article['label_description']  + ',' \
                        + article['Possible_ER_from_Article_Name'] +','+ article["possible_ER_from_Comprehend"]+','+article['batch']
                        rf.write(arti+'\n')
                        if 'IPOs' in article['label_for_article_name']  or 'Bankruptcy' in article['label_for_article_name']:
                            create_file_bankruptcy_IPO(today_date, arti)
                        split_sources(arti)
                        wf2.write(timenow + ',' + article['pubDate'] + ',' +str(article['link'])+'\n')  
                        print(str(i)+ " "+arti[42:60]+'\n')                
