#!/Users/xxxxxxxxxx/.pyenv/shims/python
#
# Title: ec2_createdafter_date.py
#
# Description: ec2_createdafter.py uses aws's boto3 to make api calls to aws
# for the service's information. It captures the attachment date of the
# elastic network interface (eni) which is a good idea of creation date.
#
# Usage: ec2_createdafter_date.py [-h|<account_alias>]
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
import argparse

# parse the command line for account alias...
parser = argparse.ArgumentParser(
    description='Script to get instances created after a date. May 2019 is hardcoded')
parser.add_argument('Account', help='AWS account alias: prod, nonprod, and sandbox',
                    action="store", default='prod')
args = parser.parse_args()
account = args.Account

envkey = 'Environment'
namekey = 'Name'
stackkey = 'Stack'
# connect to aws account, ec2...
client = boto3.client('ec2')
response = client.describe_instances()

# empty list to start...
instances_after_may2019 = []

# open a .csv file to work with...
with open(account + '_instances_after_may2019.csv', mode='w') as csv_file:
    fieldnames = ['Account', 'InstanceID', 'AttachTime', 'Name', 'Stack', 'InstanceType']
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
            startdate = datetime(2019, 5, 1, tzinfo=timezone.utc)
            if attachtime > startdate:
                ec2 = boto3.resource('ec2')
                ec2instance = ec2.Instance(instanceid)
                tags = ec2instance.tags or []
                # environment = [tag.get('Value') for tag in tags if tag.get('Key') == envkey] or 'None'
                instname = [tag.get('Value')
                            for tag in tags if tag.get('Key') == namekey] or ['NoValue']
                stackname = [tag.get('Value')
                             for tag in tags if tag.get('Key') == stackkey] or ['NoValue']
                aftermay2019 = instanceid + ',' + str(attachtime) + ',' + instancetype
                writer.writerow({'Account': account, 'InstanceID': instanceid, 'AttachTime': attachtime,
                                'Name': instname[0], 'Stack': stackname[0], 'InstanceType': instancetype})
                instances_after_may2019.append(aftermay2019)

print(instances_after_may2019)
