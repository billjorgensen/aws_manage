#!/Users/xxxxxxxxxx/.pyenv/shims/python
import boto3
#import boto
import os
import csv
from datetime import datetime, timezone, timedelta
import argparse
#
# # parse the command line for positional arguments...
parser = argparse.ArgumentParser(
    description='Script to get Instance IDs with specific cost allocation tags')
parser.add_argument('Account', help='AWS account alias: samba, tech, sandbox, etc',
                    action="store", default='samba')
args = parser.parse_args()
account = args.Account

# client = boto3.client('ec2')
# response = client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
# print(response)
ec2client = boto3.client('ec2')
# ec2response = ec2client.describe_volumes(Filters=[{'Name': 'status', 'Values': ['in-use']}])
ec2response = ec2client.describe_volumes()
print(ec2response)

volumes_asof_aug2020 = []
with open(account + '_volumes_before_aug2020.csv', mode='w') as csv_file:
    fieldnames = ['Account', 'VolumeId', 'VolumeSize', 'VolumeType', 'VolumeState', 'CreateTime']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for volume in ec2response['Volumes']:
        volumeid = volume['VolumeId']
        volumeattachments = volume['Attachments']
        if volumeattachments == []:
            volumestate = 'available'
        else:
            volumestate = 'in-use'
        volumesize = volume['Size']
        volumetype = volume['VolumeType']
        createtime = volume['CreateTime']
#         # attachtime = attachment.get('AttachTime')
        startdate = datetime(2020, 8, 25, tzinfo=timezone.utc)
        if createtime < startdate:
            beforeaug2020 = account + ',' + volumeid + ',' + \
                str(volumesize) + ',' + volumetype + ',' + volumestate + ',' + str(createtime)
            writer.writerow({'Account': account, 'VolumeId': volumeid, 'VolumeSize': volumesize,
                            'VolumeType': volumetype, 'VolumeState': volumestate, 'CreateTime': createtime})
            volumes_asof_aug2020.append(beforeaug2020)

print(volumes_asof_aug2020)
