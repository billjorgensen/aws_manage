#!/Users/xxxxxxxxxx/.pyenv/shims/python
#
# Title: iam_getsts.py
#
# Description: iam_getsts.py uses aws python module, boto3, to make an api
# call to aws iam and get an assumed role's sts creds
#
# Usage: rds_getcreation_date.py
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

# create an STS client object that represents a live connection to the
# STS service
sts_client = boto3.client('sts')

# Call the assume_role method of the STSConnection object and pass the role
# ARN and a role session name.
assumed_role = sts_client.assume_role(
    RoleArn="arn:aws:iam::xxxxxxxxxxxx:role/AdminAccess",
    RoleSessionName="AssumedSession"
)

# From the response that contains the assumed role, get the temporary
# credentials that can be used to make subsequent API calls
credentials = assumed_role['Credentials']

ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken'],
)
response = ec2_client.describe_instances(
    Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'running',
            ]
        }
    ]
)

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        instanceid = instance["InstanceId"]
        print(instanceid)
