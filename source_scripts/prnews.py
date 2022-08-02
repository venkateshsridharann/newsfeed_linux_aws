
import re
import os
import sys
import os.path
from common_scripts import *
from datetime import datetime

sys.path.append(os.path.abspath("/home/ec2-user/newsfeeds/labeling"))
from labeling import *

def extraction(key, url,data_set,seen,today,filename,database,batch):
    soup = get_content(url,None)
    all_items = soup.find_all('item')
    all_articles = []
    article = {}
    
    for i in range(len(all_items)):
        article['title'] = cleanhtml(all_items[i].find('title').get_text())
        pubDate = all_items[i].find('pubDate').get_text()[:-6]
        pubDate = datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S')
        pubDate = pubDate.strftime("%m/%d/%Y %H:%M:%S")
        article['pubDate']=pubDate
        article['batch']=  batch
        article['link'] = all_items[i].find('link').get_text()
        article['description'] = cleanhtml(all_items[i].find('description').get_text()[3:-4])
        article['source'] = "PRNewswire -"+key
        all_articles.append(article)
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
                        + article['Possible_ER_from_Article_Name'] +','+ article["possible_ER_from_Comprehend"]+','+article['batch']
                        
                        rf.write(arti+'\n')
                        if 'IPOs' in article['label_for_article_name']  or 'Bankruptcy' in article['label_for_article_name']:
                            create_file_bankruptcy_IPO(today_date, arti)
                        wf2.write(timenow + ',' + article['pubDate'] + ',' +str(article['link'])+'\n') 
                        print(str(i)+ " "+arti[40:60]+'\n')
                        

def main_prnews(data_set,today,filename,database,batch):
    seen = set()
    urls ={'All News Releases':'https://www.prnewswire.com/rss/news-releases-list.rss',
    'Auto & Transportation':'https://www.prnewswire.com/rss/automotive-transportation-latest-news.rss',
    'Business Technology':'https://www.prnewswire.com/rss/business-technology-latest-news/business-technology-latest-news-list.rss',
    'Business Technology':'https://www.prnewswire.com/rss/business-technology-latest-news/business-technology-latest-news-list.rss',
    'Consumer Products & Retail': 'https://www.prnewswire.com/rss/consumer-products-retail-latest-news/consumer-products-retail-latest-news-list.rss',
    'Consumer Technology': 'https://www.prnewswire.com/rss/consumer-technology-latest-news/consumer-technology-latest-news-list.rss',
    'Energy': 'https://www.prnewswire.com/rss/energy-latest-news/energy-latest-news-list.rss',
    'Entertain­ment & Media': 'https://www.prnewswire.com/rss/entertainment-media-latest-news/entertainment-media-latest-news-list.rss',                   
    'Environ­ment':'https://www.prnewswire.com/rss/environment-latest-news/environment-latest-news-list.rss',
    'Financial Services & Investing':'https://www.prnewswire.com/rss/financial-services-latest-news.rss',
    'General Business':'https://www.prnewswire.com/rss/general-business-latest-news/general-business-latest-news-list.rss',
    'Heavy Industry & Manufacturing':'https://www.prnewswire.com/rss/heavy-industry-manufacturing-latest-news/heavy-industry-manufacturing-latest-news-list.rss',
    'Health':'https://www.prnewswire.com/rss/health-latest-news/health-latest-news-list.rss',
    'People & Culture':'https://www.prnewswire.com/rss/multicultural-latest-news/multicultural-latest-news-list.rss',
    'Policy & Public Interest':'https://www.prnewswire.com/rss/policy-public-interest-latest-news/policy-public-interest-latest-news-list.rss',
    'Telecomm­unications':'https://www.prnewswire.com/rss/telecommunications-latest-news/telecommunications-latest-news-list.rss',
    'Sports':'https://www.prnewswire.com/rss/sports-latest-news/sports-latest-news-list.rss',
    'Travel':'https://www.prnewswire.com/rss/travel-latest-news/travel-latest-news-list.rss'}
    
    for key in urls:
        extraction(key, urls[key],data_set,seen,today,filename,database,batch)



    
# main_prnews(data_set)
