from common_scripts import *

def main_axios(driver,data_set,today_date,filename,database,batch):
     
    driver.get('https://www.axios.com/newsletters/axios-pro-rata')
    driver.implicitly_wait(100)
    html = driver.page_source
    html = BeautifulSoup(html,'lxml')
    now = datetime.now()    
    timenow = now.strftime("%m/%d/%Y %H:%M:%S")
    d = {}
    soup = html.find("div",{"class":"Newsletter__NewsletterCards-sc-111ljb9-2 faRCzk"})
    
    with open(database, "a", encoding='utf8') as rf:
            with open(filename, 'a', encoding='utf8') as wf2:                    
                for i in range(2,9):
                    deals = soup.findChildren("div" , recursive=False)[i].findChildren('div', recursive='False')[1]
                    deals = deals.find('div',{'class':'StoryText__StyledStoryText-b0w77w-0 ioucAl story-text gtm-story-text'}).findChildren('p')
                    for deal in deals:
                        d['title'] = ", ".join([x.get_text() for x in deal.find_all('strong')])
                        d['title'] = cleanhtml(d['title'].replace("•,", ""))
                        description = deal.get_text()
                        numbers = set([x for x in range(48,58,1)])
                        caps = set([x for x in range(65,91,1)])
                        lower = set([x for x in range(97,123,1)])
                        special = set([24,21,20,22,26,28,29,40])
                        allowed = numbers | caps | special | lower
                        while len(description) >0 and ord(description[0]) not in allowed:
                            description = description[1:]
                        d['description'] = cleanhtml(description)
                        d['link'] = deal.find('a')
                        if d['link']:
                            d['link'] = deal.find('a').get_text()          
                        d['pubDate'] = timenow
                        d['source'] = 'Axios'
                        d['Batch'] = batch
                        article = label_creator(d)
                        nkw = '(No Keywords detect)'
                        if article['label_for_article_name'] == nkw and article['label_description'] == nkw:
                            pass
                        else:
                            arti = timenow+ ','+ article['pubDate'] + ',' +article['source'] +','+article['title']+","+ str(article['link']) + \
                            ',' + article['description'] + ',' + article['label_for_article_name']  + ',' + article['label_description']  + ',' \
                            + article['Possible_ER_from_Article_Name'] + ','+ article["possible_ER_from_Comprehend"] +','+article['Batch']
                            rf.write(arti+'\n')
                            if 'IPOs' in article['label_for_article_name']  or 'Bankruptcy' in article['label_for_article_name']:
                                create_file_bankruptcy_IPO(today_date, arti)
                            rf.write(arti+'\n')
                            wf2.write(timenow + ',' + d['pubDate'] + ',' +str(d['link'])+'\n')  
                        d ={}
