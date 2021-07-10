#!/Users/xxxxxxxxxx/.pyenv/shims/python
#
# Title: ec2_stopnotify.py
#
# Description: ec2_stopnotify.py sources a yaml file (ec2ids_tostop.yml) with a
# list of ec2 instance ids. it uses a boto3 api call to stop the list of ec2 ids
# found running...
#
# Example ec2ids_tostop.yml
# ---
# # prod instances
# - i-xxxxxxxxxxxxxxxx
# - i-xxxxxxxxxxxxxxxx
# - i-xxxxxxxxxxxxxxxx
# - i-xxxxxxxxxxxxxxxx
#
# Usage: ec2_stopnotify.py
#
# Prerequisites:
# - python 3.7.x
# - boto3
# - appropriate aws iam privs to stop and start ec2 instances
# - aws access and secret access keys exported as linux shell environment vars
#   - AWS_DEFAULT_REGION=xx-xxxx-x
#   - AWS_DEFAULT_OUTPUT=json
#   - AWS_ACCESS_KEY_ID=xxxxxxxxxxxxxxxxxxxx
#   - AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#   - AWS_SESSION_TOKEN=<very_long_string>
# - pip installed
# - pyyaml installed
#
################################################################################
# imports...
import boto3
from botocore.exceptions import ClientError
# import time
import yaml
import smtplib
# from datetime import datetime, timezone, timedelta, date
# import os
# import sys

# function definitions
#################################################################
# send an email with instances running


def mail_running():
    text = 'nonprod InstanceIds running: ' + instancestring
    subject = 'running instances'
    smtp = smtplib.SMTP('dig MX somecompany.com', 25)
    sender = 'noreply@c7n02.somedomain.biz'
    receiver = ['someperson@somecompany.com', 'someperson@somecompany.com',
                'someperson@somecompany.com', 'someperson@somecompany.com']

    message = 'Subject: {}\n\n{}'.format(subject, text)
    try:
        smtp.sendmail(sender, receiver, message)
        print("Email sent")
        smtp.quit()
    except smtplib.ConnectionRefusedError as e:
        print("Failed to connect to email server")

# stop running instances


def stop_running():
    try:
        ec2response = ec2client.stop_instances(InstanceIds=instanceids, DryRun=False)
        print(ec2response)
    except ClientError as e:
        print(e)


#################################################################
# main
# list of instance ids...
with open('/root/scripts/ec2ids_tostop.yml') as manifest:
    ec2ids = yaml.load(manifest, Loader=yaml.FullLoader)

# connect to aws ec2...
ec2client = boto3.client('ec2')

ec2response = ec2client.describe_instances(
    Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'running',
            ]
        }
    ],
    InstanceIds=ec2ids
)

# define lists and strings...
instanceids = []
instancestring = ''

# loop through to build the list...
for reservation in ec2response['Reservations']:
    for instance in reservation['Instances']:
        instanceid = instance['InstanceId']
        instanceids.append(instanceid)
        print(instanceids)

# if nothing running, report it...
if len(instanceids) == 0:
    print('Empty list: ' + str(instanceids))
# else stop it/them and send email...
else:
    # convert a list to a string for stop_instances using list comprehension
    instancestring = ' '.join(instanceids)
    print('InstanceIds running:' + instancestring)
    stop_running()
    mail_running()
