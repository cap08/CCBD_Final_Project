import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # TODO implement
    user_id=event['user_id']
    dynamodb=boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('user-details')
    job_id=event['job_id']
    try:
        table.update_item(
                Key={'user_id':user_id },
                UpdateExpression="SET liked_jobs.#job_name = :val",
                ExpressionAttributeNames={"#job_name": job_id},
                ExpressionAttributeValues={':val': '1'},
                ReturnValues="ALL_NEW")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ValidationException':
            response = table.update_item(
                Key={"user_id": user_id},
                UpdateExpression="set liked_jobs = :liked_jobs",
                ExpressionAttributeValues={
                ':liked_jobs': {
                    job_id: "1"
                }
            },
            ReturnValues="UPDATED_NEW"
        )
    
    
    response=table.get_item(Key={'user_id': user_id})
    print(response)
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
