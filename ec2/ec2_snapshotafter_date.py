#!/Users/xxxxxxxxxx/.pyenv/shims/python
#
# Title: ec2_snapshotafter_date.py
#
# Description: ec2_snapshotafter.py uses aws's boto3 to make api calls to aws
# for the service's information. It captures the create date of the
# elastic network interface (eni) which is a good idea of creation date.
#
# Usage: ec2_snapshotafter_date.py [-h|<account_alias>]
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
from botocore.exceptions import ClientError

# parse the command line for account alias...
parser = argparse.ArgumentParser(
    description='Script to get EBS snapshots created before a date. Aug 2019 is hardcoded')
parser.add_argument('Account', help='AWS account alias: prod, nonprod, and sandbox',
                    action="store", default='prod')
args = parser.parse_args()
account = args.Account

envkey = 'Environment'
namekey = 'Name'
stackkey = 'Stack'
# connect to aws account, ec2...
ec2client = boto3.client('ec2')
ec2response = ec2client.describe_snapshots(
    OwnerIds=[
        'self',
    ]
)

# empty list to start...
snapshots_before_apr2020 = []

# open a .csv file to work with...
with open(account + '_snapshots_before_apr2020.csv', mode='w') as csv_file:
    fieldnames = ['Account', 'SnapshotID', 'SnapName',
                  'CreateTime', 'VolumeSize', 'Environment', 'Stack']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for snapshot in ec2response["Snapshots"]:
        snapid = snapshot["SnapshotId"]
        volsize = snapshot["VolumeSize"]
        createtime = snapshot["StartTime"]
        startdate = datetime(2020, 4, 1, tzinfo=timezone.utc)
        # if createtime > startdate:
        if createtime < startdate:
            ec2res = boto3.resource('ec2')
            snapinstance = ec2res.Snapshot(snapid)
            tags = snapinstance.tags or []
            snapname = [tag.get('Value')
                        for tag in tags if tag.get('Key') == namekey] or ['NoValue']
            envname = [tag.get('Value') for tag in tags if tag.get('Key') == envkey] or ['NoValue']
            stackname = [tag.get('Value')
                         for tag in tags if tag.get('Key') == stackkey] or ['NoValue']
            beforeapr2020 = str(snapid) + ',' + str(createtime)
            writer.writerow({'Account': account, 'SnapshotID': snapid,
                            'SnapName': snapname[0], 'CreateTime': createtime, 'VolumeSize': volsize, 'Environment': envname[0], 'Stack': stackname[0]})
            snapshots_before_apr2020.append(beforeapr2020)
            # try:
            # snapresponse = ec2client.delete_snapshot(
            # SnapshotId=snapid,
            # )
            # print(snapresponse)
            # except ClientError as e:
            #print('Client error: ' + str(e))

print(snapshots_before_apr2020)
