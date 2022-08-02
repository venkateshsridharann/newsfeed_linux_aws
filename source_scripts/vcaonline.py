
import os 
import sys
from common_scripts import *
from datetime import datetime

sys.path.append(os.path.abspath("/home/ec2-user/newsfeeds/labeling"))
from labeling import *
url = 'https://www.vcaonline.com/news/rss/index.asp'


def main_vcaonline(data_set,today,filename,database,batch):
   
    seen =set()
    soup = get_content(url,None)
    all_items = soup.find_all('item')
    all_articles = []
    article = {}

    for idx in range(len(all_items)):
        
        title = all_items[idx].find('title').get_text()
        category = all_items[idx].find('category').get_text()
        article['title'] = '('+category+') '+ title
        article['link'] = all_items[idx].find('link').get_text()
        pubDate = all_items[idx].find('pubDate').get_text()[:-13]
        pubDate = datetime.strptime(pubDate, '%a, %d %b %Y')
        pubDate = pubDate.strftime("%m/%d/%Y %H:%M:%S")
        article['pubDate'] = pubDate
        article['batch'] = batch
        article['description'] = ""
        article['source'] = 'vcaonline'
        
        all_articles.append(article)
        article = {}


    with open(database, "a", encoding='utf8') as rf:
        now = datetime.now()
        timenow = now.strftime("%m/%d/%Y %H:%M:%S")

        with open(filename, 'a', encoding='utf8') as wf2:
            for i,article in enumerate(all_articles):
                if str(article['link']) not in data_set and str(article['link']) not in seen:
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
