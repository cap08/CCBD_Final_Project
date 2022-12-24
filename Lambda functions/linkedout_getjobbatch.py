import json
import boto3


def lambda_handler(event, context):
    # TODO implement
    print(event)
    job_list=event["job_ids"]
    print(job_list)
    dynamodb=boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('jobs')
    output=[]
    for value in job_list:
        job_id=value
        print(job_id)
        response = table.get_item(Key={'job_id': str(value)})
        print(response)
        output.append(response['Item'])
    return output
    print(output)
        # details=response['Item']

