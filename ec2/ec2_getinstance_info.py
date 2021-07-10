#!/Users/xxxxxxxxxx/.pyenv/shims/python
#
# Title: ec2_getinstance_info.py
#
# Description: ec2_instance_info.py uses aws's boto3 to make api calls to aws
# for the service's information. It captures instance information helpful
#
# Usage: ec2_getinstance_info.py [ account name]
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
import csv
import argparse

# parse the command line for account alias...
parser = argparse.ArgumentParser(description='Script to get instance information')
parser.add_argument('Account', help='AWS account alias: prod, nonprod and sandbox',
                    action="store", default='prod')
args = parser.parse_args()
account = args.Account
envkey = 'Environment'
namekey = 'Name'
stackkey = 'Stack'

# connect to aws account, ec2, and look for running instances...
client = boto3.client('ec2')
response = client.describe_instances(
    # Filters = [
    #     {
    #         'Name': 'instance-state-name',
    #         'Values': [
    #             'running',
    #         ]
    #     }
    # ]
)

# empty list to start...
instance_info = []

# open a .csv file to work with...
with open(account + '_instance_info.csv', mode='w') as csv_file:
    fieldnames = ['Account', 'InstanceID', 'InstanceType',
                  'OS', 'Environment', 'Stack', 'Name', 'AZ']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instanceid = instance["InstanceId"]
            instancetype = instance["InstanceType"]
            ec2 = boto3.resource('ec2')
            ec2instance = ec2.Instance(instanceid)
            platform = ec2instance.platform or 'linux'
            tags = ec2instance.tags or []
            environment = [tag.get('Value')
                           for tag in tags if tag.get('Key') == envkey] or ['NoValue']
            instname = [tag.get('Value')
                        for tag in tags if tag.get('Key') == namekey] or ['NoValue']
            stackname = [tag.get('Value')
                         for tag in tags if tag.get('Key') == stackkey] or ['NoValue']
            placement = ec2instance.placement
            azone = placement['AvailabilityZone']
            accntinstance = instanceid + ',' + instancetype
            writer.writerow({'Account': account, 'InstanceID': instanceid, 'InstanceType': instancetype, 'OS': platform,
                            'Environment': environment[0], 'Stack': stackname[0], 'Name': instname[0], 'AZ': azone})
            instance_info.append(accntinstance)

print(instance_info)
