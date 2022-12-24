import json
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

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
    searchData = es.search({"query": {"terms": {"keywords.keyword": [keyword]}}})
    resp.append(searchData)
    output=[]
    for r in resp:
        for val in r['hits']['hits']:
                key = val['_source']['job_id']
                print(key)
                if key not in output:
                    output.append(key)
    return output

def lambda_handler(event, context):
    # TODO implement
    keyword=event["queryStringParameters"]["q"]
    dynamodb=boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('jobs')
    output=es_jobs(keyword)
    ids={}
    res=[]
    for id in output:
        #print(id)
        ids={}
        response=table.get_item(Key={'job_id': str(id)})
        ids['id']=id
        ids['title']=response['Item']['title']
        ids['company']=response['Item']['company']
        res.append(id)
   
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(res)
    }
