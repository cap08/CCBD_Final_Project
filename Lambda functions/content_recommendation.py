import json
import boto3
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

def es_jobs(keyword):
    region='us-east-1'
    credentials = boto3.Session().get_credentials()
    host='search-job-xxoyysvfpqvxiaio5rmxjw2zdi.us-east-1.es.amazonaws.com'
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)
    es = Elasticsearch(
         hosts = [{'host': host, 'port': 443}],
         http_auth = awsauth,
         use_ssl = True,
         verify_certs = True,
         connection_class = RequestsHttpConnection
     )
    resp=[]
    searchData = es.search({"query": {"terms": {"keywords.keyword": keyword}}})
    resp.append(searchData)
    output=[]
    for r in resp:
        for val in r['hits']['hits']:
                key = val['_source']['job_id']
                if key not in output:
                    output.append(key)
    return output
    

def lambda_handler(event, context):
    # TODO implement
    user_id=event['user_id']
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('user-details')
    response = table.get_item(Key={'user_id': user_id})
    #response contains keywords
    print(response)
    keyword=response['Item']['skills_textract']
    print(keyword)
    output=es_jobs(keyword)
    print(output)
    #output has job ids
    table_jobs=dynamodb.Table('jobs')
    results=[]
    for id in output:
        results.append(table_jobs.get_item(Key={'job_id': str(id)}))
    print(results) #job-id, url and ti
    body={'job_details':output}
    return {
        'statusCode': 200,
        'body': body
    }
