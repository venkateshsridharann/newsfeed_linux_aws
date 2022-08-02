import os
import boto3

s3 = boto3.client('s3')


def download_prev_seen(date):
    year_month = date[:-3]
    file_in_s3 = 'previously_seen_{}.csv'.format(year_month)
    try:
        s3.head_object(Bucket='aws-venky-newsfeeds', Key='previous/previously_seen_{}.csv'.format(year_month))
        if not os.path.exists('/home/ec2-user/newsfeeds/tmp'):
            os.makedirs('/home/ec2-user/newsfeeds/tmp')
        file_save_as = '/home/ec2-user/newsfeeds/tmp/'+file_in_s3
        s3.download_file('aws-venky-newsfeeds', 'previous/'+file_in_s3, file_save_as)
        print('Downloaded '+file_in_s3+'\n')
    except:
        print(file_in_s3+' File not downloaded\n')


def download_database(year_month_date):
    file_in_s3 = 'database_{}.csv'.format(year_month_date)
    try:
        s3.head_object(Bucket='aws-venky-newsfeeds', Key='database/database_{}.csv'.format(year_month_date))
        if not os.path.exists('/home/ec2-user/newsfeeds/tmp'):
            os.makedirs('/home/ec2-user/newsfeeds/tmp')
        file_save_as = '/home/ec2-user/newsfeeds/tmp/'+file_in_s3
        s3.download_file('aws-venky-newsfeeds', 'database/'+file_in_s3, file_save_as)
        print('Downloaded '+file_in_s3+'\n')
    except:
        print(file_in_s3+' File not downloaded\n')


def download_bankruptcy_ipo(year_month_date):
    file_in_s3 = 'bankruptcy_ipo_{}.csv'.format(year_month_date)
    try:
        s3.head_object(Bucket='aws-venky-newsfeeds', Key='bankruptcy_ipo/bankruptcy_ipo_{}.csv'.format(year_month_date))
        if not os.path.exists('/home/ec2-user/newsfeeds/tmp'):
            os.makedirs('/home/ec2-user/newsfeeds/tmp')
        file_save_as = '/home/ec2-user/newsfeeds/tmp/'+file_in_s3
        s3.download_file('aws-venky-newsfeeds', 'bankruptcy_ipo/'+file_in_s3, file_save_as)
        print('Downloaded '+file_in_s3+'\n')
    except:
        print(file_in_s3+' File not downloaded\n')


def download_from_s3(date):
    download_database(date)
    download_prev_seen(date)
    download_bankruptcy_ipo(date)
