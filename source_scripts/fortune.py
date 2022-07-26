import re
import os
import sys
import time 
import requests
import pandas as pd
from lxml import html
from common_scripts import *
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

sys.path.append(os.path.abspath("..\labeling"))
from labeling import *

sys.path.append(os.path.abspath("..\\boto3"))


def main_fortune(driver,today_date,database):
    url = 'https://fortune.com/newsletter/termsheet/'
    driver.get(url)
    driver.implicitly_wait(100)
    html = driver.page_source
    html = BeautifulSoup(html,'lxml')
    page = html.find('center').find('table', {'id':'templateContainer'}).find('tbody').find_all(recursive=False)
    page = page[2].find('div').findChildren('p', recursive=False)
    now = datetime.now()
    timenow  = now.strftime("%m/%d/%Y %H:%M:%S")
    deals = page[:-3]
    d = {}
    with open(database, "a", encoding='utf8') as rf:
        for i,deal in enumerate(deals):
            d['source'] = 'Fortune'
            d['title']  = cleanhtml(deal.get_text()[1:])
            d['description'] =''
            article = label_creator(d)
            
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
                print(str(i)+ " "+arti[42:60]+'\n')
                d ={}


