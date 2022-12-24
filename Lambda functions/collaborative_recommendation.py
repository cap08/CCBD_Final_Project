import json
import boto3

def lambda_handler(event, context):
    
    client = boto3.client('personalize-runtime')
    
    user_id=event['user_id'] #Cognito
    
    response = client.get_recommendations(campaignArn='arn:aws:personalize:us-east-1:725740804677:campaign/recommend',
    userId=user_id ,numResults=8)
    print(response)
    dynamodb=boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('jobs')
    rec_jobs=[]
    #resp=table.get_item(Key={'job_id':'556566'})
    for i in range(len(response['itemList'])):
        #result = table.get_item(Key={'job_id': response['itemList'][i]['itemId']})
        #print(result)
        rec_jobs.append(response['itemList'][i]['itemId'])
    print(rec_jobs)
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': rec_jobs 
    }
