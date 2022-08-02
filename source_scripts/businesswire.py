import os
import sys
from lxml import html
from common_scripts import *
from datetime import datetime

sys.path.append(os.path.abspath("/home/ec2-user/newsfeeds/labeling"))
from labeling import *
# add all sourses
urls = {'Merger':'https://feed.businesswire.com/rss/home/?rss=G1QFDERJXkJeEFtRWA==',
        'Funding':'https://feed.businesswire.com/rss/home/?rss=G1QFDERJXkJeEFtRXw==',
        'IPO':'https://feed.businesswire.com/rss/home/?rss=G1QFDERJXkJeEF9YXQ==',
        'Divestiture':'https://feed.businesswire.com/rss/home/?rss=G1QFDERJXkJeGVtWXQ==',
        'Bankruptcy':'https://www.businesswire.com/portal/site/home/news/subject/?vnsId=31318'}


  
def extraction(i,action, url,data_set,seen,today,filename,database,batch):
    soup = get_content(url,None)
    all_items = soup.find_all('item')
    all_articles = []
    article = {}
    # print(data_set)
    for idx in range(len(all_items)):
        
        article['title'] = cleanhtml(all_items[idx].find('title').get_text())
        link = all_items[idx].find('link').get_text()
        if '?feedref=' in link:
            link = link[:link.find('?feedref=')]        
        article['link'] =link
        pubDate = all_items[idx].find('pubDate').get_text()[:-3]
        pubDate = datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S')
        pubDate = pubDate.strftime("%m/%d/%Y %H:%M:%S")
        article['pubDate'] = pubDate
        article['batch'] = batch
        article['description'] = cleanhtml(all_items[idx].find('description').get_text())
        all_articles.append(article)
        article['source'] = 'Businesswire '+ action
        article = {}


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
                        + article['Possible_ER_from_Article_Name'] +','+ article["possible_ER_from_Comprehend"] +','+article['batch']
                        rf.write(arti+'\n')
                        if 'IPOs' in article['label_for_article_name']  or 'Bankruptcy' in article['label_for_article_name']:
                            create_file_bankruptcy_IPO(today_date, arti)
                        wf2.write(timenow + ',' + article['pubDate'] + ',' +str(article['link'])+'\n') 
                        print(str(i)+ " "+arti[40:60]+'\n')
                
                    
                    

def main_businesswire(data_set,today,filename,database,batch):
    seen =set()
    for i,key in enumerate(urls) :
        extraction(i,key,urls[key],data_set,seen,today,filename,database,batch)
      
