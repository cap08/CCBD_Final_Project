import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    user_id=event['user_id']
    print(user_id)
    dynamodb=boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('user-details')
    job_id=event['job_id']
    response=table.get_item(Key={'user_id': user_id})
    print(response)
    table.update_item(
                Key={'user_id':user_id},
                UpdateExpression="REMOVE liked_jobs.#job_id",
                ExpressionAttributeNames={"#job_id": job_id},
                ReturnValues="UPDATED_NEW")
    response=table.get_item(Key={'user_id': user_id})
    print(response)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
