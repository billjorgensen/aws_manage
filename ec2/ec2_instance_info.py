#!/Users/xxxxxxxxxx/.pyenv/shims/python
import boto3
import boto
import os
import csv
import argparse
from datetime import datetime, timezone, timedelta
# import argparse
#
# # parse the command line for positional arguments...
parser = argparse.ArgumentParser(
    description='Script to get Instance IDs with specific cost allocation tags')
parser.add_argument('Account', help='AWS account alias: xxxxx, tech, sandbox, etc',
                    action="store", default='xxxxx')
args = parser.parse_args()
account = args.Account
envkey = 'Environment'
namekey = 'Name'
stackkey = 'Stack'

client = boto3.client('ec2')
# response = client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
response = client.describe_instances()
# print(response)

instances_asof_sep2020 = []
with open(account + '_instances_info.csv', mode='w') as csv_file:
    fieldnames = ['Account', 'Name', 'InstanceId', 'InstanceType',
                  'Environment', 'Stack']  # , 'AvailabilityZone']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # availz = instance['Placement']['AvailabilityZone']
            # oper = instance['Platform'] or ['linux']
            instance_type = instance['InstanceType']
            instance_id = instance['InstanceId']
            # network is a list of nested dictionaries...
            networkinterface = instance['NetworkInterfaces']
            # print(networkinterface)
            # attachments = networkinterface[0]
            # # attachtime = attachments['AttachTime']
            # print(attachments)
            # attachtime = attachments.get('Attachment').get('AttachTime')
            # startdate = datetime(2020, 9, 9, tzinfo=timezone.utc)
            ec2res = boto3.resource('ec2')
            ec2instance = ec2res.Instance(instance_id)
            tags = ec2instance.tags or []
            environment = [tag.get('Value')
                           for tag in tags if tag.get('Key') == envkey] or ['NoValue']
            instname = [tag.get('Value')
                        for tag in tags if tag.get('Key') == namekey] or ['NoValue']
            stackname = [tag.get('Value')
                         for tag in tags if tag.get('Key') == stackkey] or ['NoValue']
            # if attachtime < startdate:
            asofsep2020 = instname[0] + ',' + instance_id + ',' + \
                instance_type + ',' + environment[0] + ',' + stackname[0]
            writer.writerow({'Account': account, 'Name': instname[0], 'InstanceId': instance_id, 'InstanceType': instance_type,
                            'Environment': environment[0], 'Stack': stackname[0]})  # , 'AvailabilityZone': availz})
            instances_asof_sep2020.append(asofsep2020)

print(instances_asof_sep2020)
