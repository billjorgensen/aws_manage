#!/Users/xxxxxxxxx/.pyenv/shims/python
#
# Title: ec2_create_date.py
#
# Description: ec2_create_date.py uses aws's boto3 to make api calls to aws
# for the service's information. It captures the attachment date of the
# elastic network interface (eni) which is a good idea of creation date.
#
# Usage: ec2_create_date.py
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

client = boto3.client('ec2')
response = client.describe_instances()

instances_after_jan2019 = []
with open('instances_after_jan2019.csv', mode='w') as csv_file:
    fieldnames = ['InstanceID', 'AttachTime', 'InstanceType']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instanceid = instance["InstanceId"]
            instancetype = instance["InstanceType"]
            # network is a list of nested dictionaries...
            networkinterface = instance["NetworkInterfaces"]
            attachment = networkinterface[0]
            attachtime = attachment.get('Attachment').get('AttachTime')
            startdate = datetime(2019, 1, 1, tzinfo=timezone.utc)
            if attachtime > startdate:
                afterjan2019 = instanceid + ',' + str(attachtime) + ',' + instancetype
                writer.writerow({'InstanceID': instanceid, 'AttachTime': attachtime, 'InstanceType': instancetype})
                instances_after_jan2019.append(afterjan2019)

print(instances_after_jan2019)
