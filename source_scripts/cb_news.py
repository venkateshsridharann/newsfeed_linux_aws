import re
import os
import sys
import os.path
import requests
from common_scripts import *
from datetime import datetime
from bs4 import BeautifulSoup
sys.path.append(os.path.abspath("../labeling"))
from labeling import *


def extraction(driver,key,url,data_set,seen,today,filename,database,batch):
    
    driver.get(url)
    driver.implicitly_wait(100)
    html = driver.page_source
    soup = BeautifulSoup(html, 'xml')
    soup = soup.find('div', {'class':'row row-eq-height herald-posts'})
    all_items = soup.find_all('article')
     
    all_articles = []
    article = {}
    
    for i in range(len(all_items)):
        
        header = all_items[i].find('div',{'class':"entry-header"}).find('h2')
        article['title'] = cleanhtml(header.find('a').get_text())
        try :
            pubDate =  all_items[i].find('div',{'class':"entry-header"}).find('div', {'class':'entry-meta'}) \
                .find('div', {'class':'meta-item herald-date'}).get_text()
            # print(article['title'])
            pubDate = datetime.strptime(pubDate, '%B %d, %Y')
            pubDate = pubDate.strftime("%m/%d/%Y %H:%M:%S")
        except:
            break
        article['pubDate']=pubDate
        article['link'] = header.find('a')['href']
        description = all_items[i].find('div',{'class':'entry-content'}).get_text().replace('\n','')
        article['description']  = cleanhtml(description)
        article['source'] = "Crunchbase News-"+key
        article['batch'] =batch
        all_articles.append(article)
        article = {}
    # print(all_articles)
    with open(database, "a", encoding='utf8') as rf:
        now = datetime.now()
        timenow = now.strftime("%m/%d/%Y %H:%M:%S")
        with open(filename, 'a', encoding='utf8') as wf2:
            for i,article in enumerate(all_articles):
                if str(article['link']) not in data_set and str(article['link']) not in seen :
                    seen.add(str(article['link']))
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
                        wf2.write(timenow + ',' + article['pubDate'] + ',' +str(article['link'])+'\n') 
                        print(str(i)+ " "+arti[40:60]+'\n')
         


def main_cb_news(driver,data_set,today,filename,database,batch):

    seen = set()
    urls ={'Business':'https://news.crunchbase.com/sections/business/',
    'Startups':'https://news.crunchbase.com/sections/startups/',
    'Venture':'https://news.crunchbase.com/sections/venture/' ,
    'Liquidity':'https://news.crunchbase.com/sections/liquidity/',
    'Public':'https://news.crunchbase.com/sections/public/',
    }
    
    for key in urls:
        extraction(driver,key,urls[key],data_set,seen,today,filename,database,batch)   
