import re
import unidecode
import requests
from bs4 import BeautifulSoup
from datetime import time, datetime



def get_content(url, params=None):
    response = requests.get(url, params=params)
    html = response.content
    soup = BeautifulSoup(html, 'xml')
    # soup = soup.encode("utf-8")
    return soup


def cleanhtml(raw_html):
    # removes unwanted tags
  cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});') 
#   removes unwanted newline tags
  clean_new_line = re.compile('\n')
  cleantext = re.sub(cleanr, '', raw_html)
  cleantext = re.sub(clean_new_line, '', cleantext)
  cleantext = cleantext.replace("[&#8230;]","")
  cleantext = cleantext.replace(",","")
  cleantext = unidecode.unidecode(cleantext)
  return cleantext

def create_file_bankruptcy_IPO(today_date, arti):
  bank = '..\database\\bankruptcy_ipo_{}.csv'.format(today_date)
  with open(bank, "a", encoding="utf8") as bnk :
    bnk.write(arti+'\n')


