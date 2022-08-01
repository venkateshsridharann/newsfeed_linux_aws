import os
import sys
from common_scripts import *
from datetime import datetime

sys.path.append(os.path.abspath("../labeling"))
from labeling import *

def extraction(url,data_set,seen,today_date,filename,database,batch):
    # seen = set()
    soup = get_content(url,'lxml')
    all_items = soup.find_all('item')
    all_articles = []
    article = {}

    articles_soup = soup.find("div", {"id": "benzinga-article-area-wrapper"})
    articles_soup = articles_soup.find("div", {"class": "benzinga-articles benzinga-articles-mixed"})
    articles_soup =articles_soup.find_all('li')
    # looping over all articles

    for list_item in articles_soup:
        article['title'] = cleanhtml(list_item.find('h3').get_text().strip('\n'))
        link = list_item.find('h3').find('a')['href']
        article['link'] = 'https://www.benzinga.com' + link
        pubDate = list_item.find('span', {'class':'date'}).get_text()[:20]
        if pubDate[-1] == " ":
            pubDate = datetime.strptime(pubDate, '%Y %b %d, %I:%M%p ')
        else:
            pubDate = datetime.strptime(pubDate, '%Y %b %d, %I:%M%p')
        pubDate = pubDate.strftime("%m/%d/%Y %H:%M:%S")
        article['pubDate'] = pubDate
        article['Batch'] = batch
        article['description'] = cleanhtml(list_item.find('p').get_text().replace("\n", ' ').strip(' '))
        article['source'] ="Benzinga"
        # print( article['description'] )
        all_articles.append(article)
        article = {}
    
    now = datetime.now()    
    timenow = now.strftime("%m/%d/%Y %H:%M:%S")
    
    with open(database, "a", encoding='utf8') as rf:
        with open(filename, 'a', encoding='utf8') as wf2:
            for i,article in enumerate(all_articles):
                if str(article['link']) not in data_set and str(article['link']) :
                    article = label_creator(article)
                    nkw = '(No Keywords detect)'
                    if article['label_for_article_name'] == nkw and article['label_description'] == nkw:
                        pass
                    else:    
                        arti = timenow+ ','+ article['pubDate'] + ',' +article['source'] +','+article['title']+","+ str(article['link']) + \
                        ',' + article['description'] + ',' + article['label_for_article_name']  + ',' + article['label_description']  + \
                        ',' + article['Possible_ER_from_Article_Name'] + ','+ article["possible_ER_from_Comprehend"] +','+article['Batch']
                        
                        rf.write(arti+'\n')
                        if 'IPOs' in article['label_for_article_name']  or 'Bankruptcy' in article['label_for_article_name']:
                            create_file_bankruptcy_IPO(today_date, arti)
                        wf2.write(timenow + ',' + article['pubDate'] + ',' +str(article['link'])+'\n')  
                        print(str(i)+ " "+arti[42:60]+'\n')



def main_benzinga(data_set,today,filename,database):
    seen = set()
    # the second link used for pages 1 -16 in benzinga news
    urls = ['https://www.benzinga.com/news', 'https://www.benzinga.com/news']
    
    for i,url in enumerate(urls):
        if i == 0:
            extraction(url,data_set,seen,today,filename,database) 
        if i == 1 :
            for j in range(1,16,1):
                paged_url = url +'?page='+str(j)
                extraction(paged_url,data_set,seen,today,filename,database) 
                