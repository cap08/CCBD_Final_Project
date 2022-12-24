import json
import urllib.parse
import boto3
import base64
from urllib.parse import urlparse

textract = boto3.client('textract')
comprehend = boto3.client('comprehend')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):

    # Get the object from the event and show its content type
    print(event['Records'])
    bucket = event['Records'][0]['s3']['bucket']['name']
    s3object = event['Records'][0]['s3']
    bucket = s3object['bucket']['name']
    key = s3object['object']['key']
    print(bucket, key)
    s3 = boto3.client('s3')

    try:
        extracted_data = []
        resp = s3.get_object(Bucket=bucket, Key=key)
        print(resp)
        image_bytes = resp['Body'].read()
        print(image_bytes)
        #image_test=image_bytes.decode('utf-8')
        #image_test=image_test[22:]
        #image_bytes=image_test.encode()
        #base64_image=base64.b64encode(image_bytes)
        base_64_binary = base64.decodebytes(image_bytes)
        #print(base_64_binary)
        response = textract.detect_document_text(
            Document={'Bytes': base_64_binary})
        #print(response)
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                extracted_data.append(item["Text"])
        keywords=[]
        for data in extracted_data:
            response = comprehend.detect_key_phrases(Text=data,LanguageCode='es')  
            for i in range(len(response['KeyPhrases'])):
                keywords.append(response['KeyPhrases'][i]['Text'])
        print(keywords)
        # table = dynamodb.Table('user-details')
        user_id = key[:-5]
        print(user_id)
        table = dynamodb.Table('user-details')
        response = table.get_item(
        Key={
            'user_id': user_id
        }
        )
        print(response)
        response['Item']['skills_textract'] = keywords
        print(response)
        
        table.update_item(
            Key = {'user_id': user_id},
            UpdateExpression = "SET skills_textract = :val",
            ExpressionAttributeValues={":val": keywords},
            ReturnValues="UPDATED_NEW")
        response=table.get_item(Key={'user_id':user_id})
        print(response)
        print("Updated!!")
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
