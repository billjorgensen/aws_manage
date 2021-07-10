#!/Users/xxxxxxx/.pyenv/versions/2.7.14/bin/python
import boto3
import time as t
from datetime import date, time, timedelta, datetime
import json
import logging

cwlogs = boto3.client('logs')
sqs = boto3.client('sqs')
Logs_Bucket = 's3-logging-bucket-name'
Queue_Url = 'https://sqs.us-east-1.amazonaws.com/xxxxxxxxxxxx/CloudWatchtoS3-WorkerQueue'

###############################################################################


def json_print(dict):
    print json.dumps(dict, indent=4, sort_keys=True)


def json_message(dict):
    print json.dumps(dict, indent=4, sort_keys=False)


def get_sqs_message(Queue_Url):
    http_response = sqs.receive_message(
        QueueUrl=Queue_Url,
        AttributeNames=['ApproximateFirstReceiveTimestamp', 'SentTimestamp'],
        MessageAttributeNames=['All'],
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20
    )
    if http_response.get('Messages'):
        return http_response['Messages'][0]
    else:
        return None


def is_export_task_complete(task_id):
    task_status = cwlogs.describe_export_tasks(
        taskId=task_id
    )
    task_completed = task_status['exportTasks'][0]['status']['code']
    if task_completed == 'COMPLETED':
        return True
    else:
        return False

###############################################################################


message = get_sqs_message(Queue_Url)

while message:
    receipt_handle = message['ReceiptHandle']
    body = json.loads(message['Body'])

    # capture the variables needed for cloudwatch export task...
    to_time = int(body['to'])
    from_time = int(body['fromTime'])
    log_group_name = str(body['logGroupName'])
    log_group_prefix = 'CloudWatchLogs' + log_group_name

    export_task = cwlogs.create_export_task(
        taskName=log_group_name,
        logGroupName=log_group_name,
        fromTime=from_time,
        to=to_time,
        destination=Logs_Bucket,
        destinationPrefix=log_group_prefix
    )
    task_id = export_task['taskId']

    while not is_export_task_complete(task_id):
        t.sleep(0.45)

#     message = get_sqs_message_body(Queue_Url)

    # print("EXPORT TASK COMPLETE")
    # json_print(message)
    # print('\n')

    delete_message = sqs.delete_message(
        QueueUrl=Queue_Url,
        ReceiptHandle=receipt_handle
    )

    message = get_sqs_message(Queue_Url)
