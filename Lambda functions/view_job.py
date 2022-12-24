import json
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth



def lambda_handler(event, context):
    # TODO implement
    job_id=event["job_id"]
    dynamodb=boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('jobs')
    details=[]
    ids={}
    response=table.get_item(Key={'job_id': job_id})
    print(response)
    ids['job_id']=job_id
    ids['title']=response['Item']['title']
    ids['company']=response['Item']['company']
    ids['description']=response['Item']['description']
    ids['experience_level']=response['Item']['experience_level']
    ids['location']=response['Item']['location']
    ids['url']=response['Item']['url']
    details.append(ids)
        
        
    return {
        'statusCode': 200,
        'body': details
    }

