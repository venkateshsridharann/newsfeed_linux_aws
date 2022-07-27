import os
from distutils.command import upload
import boto3

s3 = boto3.client('s3')

def upload_previous_to_aws(date):
    try:
        if os.path.isfile('..\cache\previously_seen\previously_seen_{}.csv'.format(date)):
            prev_file = 'previously_seen_{}.csv'.format(date)
            previously_seen = open("..\cache\previously_seen\\"+prev_file, 'rb')
            boto3.resource('s3').Bucket('aws-venky-newsfeeds').put_object(Key='previous/'+prev_file, Body=previously_seen)
            

    except Exception as e:
        print(e)
        print('error')

def upload_database_to_aws(date):
    try:
        if os.path.isfile('..\database\database_{}.csv'.format(date)):
            database_file = 'database_{}.csv'.format(date)
            database = open("..\database\\"+database_file, 'rb')
            boto3.resource('s3').Bucket('aws-venky-newsfeeds').put_object(Key='database/'+database_file, Body=database)
            os.remove('..\database\\database_{}.csv'.format(date))
    
    except Exception as e:
        print(e)
        print('error')

def upload_to_s3(date):
    upload_database_to_aws(date)
    upload_previous_to_aws(date[:-3])
    if os.path.isfile('..\database\database_{}.csv'.format(date)):
        os.remove('..\database\\database_{}.csv'.format(date))  
    if os.path.isfile('..\cache\previously_seen\previously_seen_{}.csv'.format(date[:-3])):
        os.remove('..\cache\previously_seen\previously_seen_{}.csv'.format(date[:-3]))
    # os.rmdir('..\cache\previously_seen')
    # os.rmdir('..\database')
    

    
    
    