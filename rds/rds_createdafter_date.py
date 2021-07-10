#!/Users/wjorgensen/.pyenv/shims/python
#
# Title: rds_createdafter_date.py
#
# Description: rds_getcreation_date.py uses aws's boto3 to make api calls to aws
# for the service's information. It gathers the creation time attribute.
#
# Usage: rds_createdafter_date.py [-h|<account_alias>]
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
    description='Script to get RDS instances created after a date. Jan 2019 is coded in')
parser.add_argument('Account', help='AWS account alias: prod, nonprod, and sandbox',
                    action="store", default='prod')
args = parser.parse_args()
account = args.Account

# envkey = 'Environment'
namekey = 'Name'
stackkey = 'Stack'
stackvalue = ''

rdsclient = boto3.client('rds')
rdsresponse = rdsclient.describe_db_instances()

rds_instances_after_may2019 = []
with open(account + '_rds_instances_after_may2019.csv', mode='w') as csv_file:
    fieldnames = ['Account', 'CreationTime', 'DBInstanceId', 'Stack', 'DBInstanceClass']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for dbinstances in rdsresponse['DBInstances']:
        dbidentifier = dbinstances['DBInstanceIdentifier']
        dbinstanceclass = dbinstances['DBInstanceClass']
        creation = dbinstances['InstanceCreateTime']
        startdate = datetime(2019, 5, 1, tzinfo=timezone.utc)
        if creation > startdate:
            rdsresponse = rdsclient.describe_db_instances(DBInstanceIdentifier=dbidentifier)
            rdsarn = rdsresponse['DBInstances'][0]['DBInstanceArn']
            rdstags = rdsclient.list_tags_for_resource(ResourceName=rdsarn)
            for key in rdstags['TagList']:
                if key['Key'] == 'Stack':
                    stackvalue = key['Value'] or 'NoValue'
            aftermay2019 = dbidentifier + ',' + str(creation) + ',' + dbinstanceclass
            writer.writerow({'Account': account, 'CreationTime': creation, 'DBInstanceId': dbidentifier,
                            'Stack': stackvalue, 'DBInstanceClass': dbinstanceclass})
            rds_instances_after_may2019.append(aftermay2019)

rdsresponse = rdsclient.describe_db_clusters()
with open(account + '_rds_clusters.csv', mode='w') as csv_file:
    fieldnames = ['Account', 'ClusterCreateTime', 'DBClusterIdentifier', 'Stack', 'EngineMode']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for dbclusters in rdsresponse['DBClusters']:
        dbidentifier = dbclusters['DBClusterIdentifier']
        dbenginemode = dbclusters['EngineMode']
        rdsarn = dbclusters['DBClusterArn']
        creation = dbclusters['ClusterCreateTime']
        startdate = datetime(2019, 5, 1, tzinfo=timezone.utc)
        if creation > startdate:
            rdstags = rdsclient.list_tags_for_resource(ResourceName=rdsarn)
            for key in rdstags['TagList']:
                if key['Key'] == 'Stack':
                    stackvalue = key['Value'] or 'NoValue'
            aftermay2019 = dbidentifier + ',' + str(creation) + ',' + dbinstanceclass
            writer.writerow({'Account': account, 'ClusterCreateTime': creation,
                            'DBClusterIdentifier': dbidentifier, 'Stack': stackvalue, 'EngineMode': dbenginemode})
            rds_instances_after_may2019.append(aftermay2019)
print(rds_instances_after_may2019)
