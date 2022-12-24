import json
import boto3

def lambda_handler(event, context):
    print(event)
    print(context)
    user_id=event['user_id']
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('user-details')
    response = table.get_item(Key={'user_id': user_id})
    return response["Item"]
