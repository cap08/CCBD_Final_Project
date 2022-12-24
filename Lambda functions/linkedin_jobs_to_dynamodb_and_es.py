import pandas as pd
import boto3
import json
import numpy as np
import csv
from botocore.vendored import requests
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

#job=pd.read_csv('/Users/sw08/Downloads/NYC_Jobs.csv')

#job.to_json('/Users/sw08/Desktop/pushtodynamodb/NYC_Jobs.json',orient='records')
#job=job.iloc[:600]
#%%
linkedin=pd.read_csv('/Users/sw08/Downloads/linkedin.csv')
#%%
linkedin.to_json('/Users/sw08/Desktop/pushtodynamodb/linkedin.json',orient='records')

#%%
with open('/Users/sw08/Desktop/pushtodynamodb/linkedin.json', 'r') as f:
        data = json.load(f)
#%%
ACCESS_ID=''
ACCESS_KEY=''

awsauth=AWS4Auth(ACCESS_ID,ACCESS_KEY,'us-east-1','es')

host = 'search-job-xxoyysvfpqvxiaio5rmxjw2zdi.us-east-1.es.amazonaws.com'

es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
) 

dynamodb = boto3.resource('dynamodb', region_name='us-east-1',aws_access_key_id=ACCESS_ID,aws_secret_access_key=ACCESS_KEY)
table = dynamodb.Table('jobs')
client=boto3.client('comprehend')

for desc in data:
    keywords=[]
    response = client.detect_key_phrases(Text=desc['Description'],LanguageCode='es')  
    for i in range(len(response['KeyPhrases'])):
        keywords.append(response['KeyPhrases'][i]['Text'])
    tableEntry = {
        'job_id': str(desc['Job_ID']),
        'company': desc['Company'],
        'title': desc['Title'],
        'experience_level': desc['Experience_level'],
        'description': desc['Description'],
        'url':desc['url'],
        'country': desc['Country'],
        'location': desc['Location'],
        'keywords': keywords
    }                
    index_data = {
        'job_id': desc['Job_ID'],
        'keywords': keywords
    }
    table.put_item(
        Item={
            'job_id': tableEntry['job_id'],
            'company': tableEntry['company'],
            'title': tableEntry['title'],
            'experience_level': tableEntry['experience_level'],
            'description': tableEntry['description'],
            'country':tableEntry['country'],
            'location':tableEntry['location'],
            'url': tableEntry['url'],
            'keywords': tableEntry['keywords']
           }
        )
    es.index(index="job", doc_type="Jobs", id=desc['Job_ID'], body=index_data, refresh=True)
#%%

