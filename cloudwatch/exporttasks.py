#!/Users/xxxxxxx/.pyenv/versions/2.7.14/bin/python
import boto3
import time as t
from datetime import date, time, timedelta, datetime
import json
import logging

LOGS_BUCKET = 'bills-logs'
cwlogs = boto3.client('logs')
sqs = boto3.client('sqs')

###############################################################################


def json_print(dict):
    print json.dumps(dict, indent=4, sort_keys=True)


def json_message(dict):
    print json.dumps(dict, indent=4, sort_keys=False)


def get_epoch(datetime_object):
    return int(datetime_object.strftime('%s'))

###############################################################################


# midnight_today_datetime = datetime.combine(date.today(), time.min)
# midnight_yesterday_datetime = midnight_today_datetime - timedelta(days=1)
#
# midnight_today_epoch = get_epoch(midnight_today_datetime)
# midnight_yesterday_epoch = get_epoch(midnight_yesterday_datetime)

#queue = sqs.get_queue_url(QueueName='')

message_body = {"logGroupName": '/aws/lambda/CloudformationEventNotifications-Function',
                "fromTime": 1519582724, "to": 1519755647}
# json_message = json_message(message_body)
# print(json_message)
send_message = sqs.send_message(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/xxxxxxxxxxxx/CloudWatchtoS3-WorkerQueue'
    MessageBody=json.dumps(message_body)
)
# message = []
# message = sqs.receive_message(
#     QueueUrl = 'https://sqs.us-east-1.amazonaws.com/xxxxxxxxxxxx/bills-test-queue',
#     #AttributeNames = [ 'All' ],
#     AttributeNames = [ 'ApproximateFirstReceiveTimestamp', 'SentTimestamp' ],
#     MessageAttributeNames = [ 'All' ],
#     MaxNumberOfMessages = 1,
#     WaitTimeSeconds = 20
# )
#
# json_print(message)
# print(type(message))

# get the message body to the point we can use it...
# sqs_message = json.loads(message['Messages'][0]['Body'])
# receipt_handle = message['Messages'][0]['ReceiptHandle']

# capture the variables needed for cloudwatch export task...
# to_time = int(sqs_message['to'])
# from_time = int(sqs_message['fromTime'])
# log_group_name = str(sqs_message['logGroupName'])
# log_group_prefix = 'CloudWatchLogs' + log_group_name
# print(to_time, from_time)
# print(log_group_name)
# print(log_group_prefix)
# print(receipt_handle)

# is_log_there = cwlogs.describe_log_groups(
#     logGroupNamePrefix = log_group_name
# )
# json_print(is_log_there)
# export_task = cwlogs.create_export_task(
#     taskName = log_group_name,
#     logGroupName = log_group_name,
#     fromTime = from_time,
#     to = to_time,
#     destination = LOGS_BUCKET,
#     destinationPrefix = log_group_prefix
# )
# delete_message = sqs.delete_message(
#     QueueUrl = 'https://sqs.us-east-1.amazonaws.com/xxxxxxxxxxxx/bills-test-queue',
#     ReceiptHandle = receipt_handle
# )
