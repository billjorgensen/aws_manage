#!/Users/xxxxxxxxx/.pyenv/shims/python
#
# Title: rds_create_date.py
#
# Description: rds_create_date.py uses aws's boto3 to make api calls to aws
# for the service's information. It gathers the creation time attribute.
#
# Usage: rds_create_date.py
#
# Requirements:
# - aws credentials properly exported as environment variables
#   Here are the variables needed to export as environment variables:
#     AWS_DEFAULT_REGION=us-east-1
#     AWS_DEFAULT_OUTPUT=json
#     AWS_ACCESS_KEY_ID=xxxxxxxxxxxxxxxxxxxx
#     AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#     AWS_SESSION_TOKEN=very long char string
# - python 3.7.* installed and used. Notice the magic number references a
#   pyenv shims path not a general python path. The version used initially
#   is 3.7.2
#
##########################################################################
import boto3
from datetime import datetime, timezone, timedelta
import csv

client = boto3.client('rds')
response = client.describe_db_instances()

rds_instances_after_jan2019 = []
with open('rds_instances_after_jan2019.csv', mode='w') as csv_file:
    fieldnames = ['DBInstanceId', 'CreationTime', 'DBInstanceClass']
    writer =csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for dbinstances in response['DBInstances']:
        dbidentifier = dbinstances['DBInstanceIdentifier']
        dbinstanceclass = dbinstances['DBInstanceClass']
        creation = dbinstances['InstanceCreateTime']
        startdate = datetime(2019, 1, 1, tzinfo=timezone.utc)
        if creation > startdate:
            afterjan2019 = dbidentifier + ',' + str(creation) + ',' + dbinstanceclass
            writer.writerow({'DBInstanceId': dbidentifier, 'CreationTime': creation, 'DBInstanceClass': dbinstanceclass})
            rds_instances_after_jan2019.append(afterjan2019)

print(rds_instances_after_jan2019)
