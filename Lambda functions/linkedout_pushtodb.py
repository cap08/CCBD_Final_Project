import json
import boto3

def lambda_handler(event, context):
    print(event)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user-details')
    # tableEntry = {
    #     'user_id': event['user_id'],
    #     'first_name': event['first_name'],
    #     'last_name': event['last_name'],
    #     'highest_deg': event['highest_deg'],
    #     'major': event['Job Description'],
    #     'year_of_grad': desc['Minimum Qual Requirements'],
    #     'liked_jobs': keywords,
    #     'interested_jobs': keywords,
    #     'skills_input': keywords,
    #     'skills_textract': keywords
    # }       
    # event["skills_textract"] = ""
    # event["liked_jobs"] = ""
    
    print(event)
    table.put_item(Item=event)
    print("Inserted")
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Insert success!')
    }
