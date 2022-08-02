import os
import re
import sys
import time  as t
from common_scripts import *
from datetime import datetime
from bs4 import BeautifulSoup
sys.path.append(os.path.abspath("/home/ec2-user/newsfeeds/labeling"))
from labeling import *

def get_articles_in_all_pages(driver,pg,data_set,seen,today,filename,database):
    url = 'https://peprofessional.com/category/news/all-news/page/'+str(pg)+'/'
    driver.get(url)
    driver.implicitly_wait(100)
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    articles = soup.find('main').find_all('article')
    all_articles =[]
    article ={}
    
    for arti in articles:
        article['title'] = cleanhtml(arti.find('h2').get_text().strip())
        article['link'] = arti.find('h2').find('a')['href']
        pubDate = arti.find('p').find('span').find('time').get_text().strip()
        pubDate = datetime.strptime(pubDate, '%B %d, %Y')
        pubDate = pubDate.strftime("%m/%d/%Y, 00:00:00")
        article['pubDate'] = pubDate
        article['description'] = arti.findChildren("p" , recursive=False)[1].get_text()
        article['source'] = 'PEProfessional'
        all_articles.append(article)
        article ={}
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
                        ',' + article['description'] + ',' + article['label_for_article_name']  + ',' + article['label_description']  + ','\
                         + article['Possible_ER_from_Article_Name'] +','+ article["possible_ER_from_Comprehend"]
                        rf.write(arti+'\n')
                        if 'IPOs' in article['label_for_article_name']  or 'Bankruptcy' in article['label_for_article_name']:
                            create_file_bankruptcy_IPO(today_date, arti)
                        wf2.write(timenow + ',' + article['pubDate'] + ',' +str(article['link'])+'\n') 
                        print(str(i)+ " "+arti[40:60]+'\n')
                
                        
def main_pep(driver,data_set,today,filename,database):  
    seen = set()      
    all_pages = 3
    for pg in range(1,all_pages+1,1):
        get_articles_in_all_pages(driver,pg,data_set,seen,today,filename,database)
        t.sleep(12)
