import os
import boto3

s3 = boto3.resource('s3')
BUCKET_NAME = 'privco-newsfeeds' 
tmp_base = '/home/ec2-user/newsfeeds/tmp/'


def download_prev_seen(date):
    year_month = date[:-3]
    file = 'previously_seen_{}.csv'.format(year_month)
    save_as = tmp_base+file
    KEY = 'previous/previously_seen_{}.csv'.format(year_month)
    try:
        print(s3.Object(BUCKET_NAME, KEY).load())
        s3.Bucket(BUCKET_NAME).download_file(KEY, save_as)
        print(file +' downloaded\n')
    except:

        print("The object does not exist. previously_seen_{} not downloaded \n".format(year_month))
        

def download_database(year_month_date):
    file = 'database_{}.csv'.format(year_month_date)
    save_as = tmp_base+file
    KEY = 'database/database_{}.csv'.format(year_month_date)
    try:
        s3.Bucket(BUCKET_NAME).download_file(KEY, save_as)
        print(file +' downloaded\n')
    except:
        print("The object does not exist. database_{} not downloaded \n".format(year_month_date))

def download_bankruptcy_ipo(year_month_date):  
    file = 'bankruptcy_ipo_{}.csv'.format(year_month_date)
    save_as = tmp_base+file
    KEY = 'bankruptcy_ipo/bankruptcy_ipo_{}.csv'.format(year_month_date)
    try:
        s3.Bucket(BUCKET_NAME).download_file(KEY, save_as)
        print(file +' downloaded\n')
    except:
        print("The object does not exist. bankruptcy_ipo_{} not downloaded \n".format(year_month_date))

def download_from_s3(date):
    download_database(date)
    download_prev_seen(date)
    download_bankruptcy_ipo(date)


