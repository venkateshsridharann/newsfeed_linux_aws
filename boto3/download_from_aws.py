import os
import boto3
from datetime import datetime
s3 = boto3.client('s3')


def download_prev_seen(year_month):
    try:
        s3.head_object(Bucket='aws-venky-newsfeeds', Key='previous/previously_seen_{}.csv'.format(year_month))
        file_in_s3 = 'previously_seen_{}.csv'.format(year_month)
        if not os.path.exists('..\cache\previously_seen'):
            os.makedirs('..\cache\previously_seen')
        file_save_as = '..\cache\previously_seen\\'+file_in_s3
        s3.download_file('aws-venky-newsfeeds', 'previous/'+file_in_s3, file_save_as)
        print('Downloaded '+file_in_s3)
    except:
        print('File not downloaded')


def download_database(year_month_date):
    try:
        s3.head_object(Bucket='aws-venky-newsfeeds', Key='database/database_{}.csv'.format(year_month_date))
        file_in_s3 = 'database_{}.csv'.format(year_month_date)
        if not os.path.exists('database'):
            os.makedirs('database')
        file_save_as = '..\database\\'+file_in_s3
        s3.download_file('aws-venky-newsfeeds', 'database/'+file_in_s3, file_save_as)
        print('Downloaded '+file_in_s3)
    except:
        print('File not downloaded')


def download_from_s3(date):
    download_database(date)
    download_prev_seen(date[:-3])