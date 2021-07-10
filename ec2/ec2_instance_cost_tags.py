#!/Users/xxxxxxxxxx/.pyenv/shims/python
#
# Title: ec2_instance_cost_tags.py
#
# Usage: ec2_instance_cost_tags.py tag_key key_value
#
# This is unique to a company's cost allocation tags. this can be modified
# for any tags desired...
##############################################################################
import boto3
import sys
import argparse

# parse the command line for positional arguments...
parser = argparse.ArgumentParser(
    description='Script to get Instance IDs with specific cost allocation tags')
parser.add_argument('CostTagKey', help='Cost allocation tag key. Stack, Environment, etc',
                    action="store", default='Stack')
parser.add_argument('CostTagValue', help='Cost allocation tag value. DEMO, PROD, etc',
                    action="store", default='PROD')
args = parser.parse_args()

# connect with aws for ec2...
ec2client = boto3.client('ec2')
response = ec2client.describe_instances(
    Filters=[
        {
            'Name': 'tag:'+args.CostTagKey,
            'Values': [args.CostTagValue]
        }
    ]
)

# empty list...
instancelist = []
for reservation in (response["Reservations"]):
    for instance in reservation["Instances"]:
        instancelist.append(instance["InstanceId"])

# print the python list...
print(instancelist)
