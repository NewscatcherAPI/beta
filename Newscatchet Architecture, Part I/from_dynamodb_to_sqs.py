import json
import boto3
import decimal
import logging
import os

tablename = 'TABLE_NAME_DYNAMODB'
queue_url = 'QUEUE_NAME'

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tablename)
sqs = boto3.client('sqs')

def lambda_handler(event, context):
    data = table.scan()['Items']
    for i in data:
        response = sqs.send_message(QueueUrl=queue_url, MessageBody=(json.dumps(i)))
    print(f'{len(data)} - messages have been sent to SQS')

#With DelaySeconds
def lambda_handler(event, context):
    data = table.scan()['Items']
    for j in range(0, number_sends): #parts of separation
        for i in data[int(len(data)*(1/number_sends)*j):int(len(data)*(1/number_sends)*(j+1))]:
            response = sqs.send_message(QueueUrl=queue_url,
                                        DelaySeconds=int((900/number_sends))*j,
                                        MessageBody=(json.dumps(i)))
    print(f'{len(data)} - messages have been sent to SQS')