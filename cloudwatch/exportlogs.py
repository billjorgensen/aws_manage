#!/Users/xxxxxxx/.pyenv/versions/2.7.14/bin/python
import boto3
from datetime import date, time, timedelta, datetime
import json
import logging

cwlogs = boto3.client('logs')

###############################################################################


def json_print(dict):
    print json.dumps(dict, indent=4, sort_keys=True)


def get_epoch(datetime_object):
    return int(datetime_object.strftime('%s'))

###############################################################################


logs_list = []

midnight_today_datetime = datetime.combine(date.today(), time.min)
midnight_yesterday_datetime = midnight_today_datetime - timedelta(days=1)

midnight_today_epoch = get_epoch(midnight_today_datetime)
midnight_yesterday_epoch = get_epoch(midnight_yesterday_datetime)

print(midnight_today_epoch, midnight_yesterday_epoch)
# print (int(midnight_yesterday_datetime.strftime('%s')), int(midnight_today_datetime.strftime('%s')))

log_group_paginator = cwlogs.get_paginator('describe_log_groups')
log_group_page_iterator = log_group_paginator.paginate()

for log_group_response in log_group_page_iterator:
    for log_groups_obj in log_group_response['logGroups']:
        logs_list.append(log_groups_obj['logGroupName'])


json_print(logs_list)
