#!/Users/xxxxxxxxxx/.pyenv/shims/python
#
# Title: ec2_startstopbyvpc.py
#
# Description: ec2_startstopbyvpc.py sources a yaml file (ec2_ids.yml) with a list
# of ec2 instance ids. it uses a boto3 api call to either start or stop the list
# of ec2 ids...
#
# Usage: ec2_startstopbyvpc.py [start|stop] [vpcid]
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
import yaml
import argparse

# get the command line argument...
parser = argparse.ArgumentParser(
    description='Stop or start EC2 instance(s) in a declared AWS VpcId')
parser.add_argument('startstop', help='use start or stop as the argument',
                    action='store', default='start')
parser.add_argument('vpcid', help='AWS VpcId to work with',
                    action='store', default='vpc-01046752293d3ee9e')
args = parser.parse_args()

# connect to aws ec2...
ec2client = boto3.client('ec2')

# get list of instance ids
ec2response = ec2client.describe_instances(
    Filters=[
        {
            'Name': 'vpc-id',
            'Values': vpcid
        }
    ]
)

# load the list of instance ids...
# with open('ec2_ids.yml') as manifest:
#     ec2ids = yaml.load(manifest, Loader=yaml.FullLoader)

# start or stop...
# if args.startstop == "start":
#     ec2response = ec2client.start_instances(
#         InstanceIds = ec2ids
#     )
#     # print the ec2response...
#     print(ec2response)
# else:
#     ec2response = ec2client.stop_instances(
#         InstanceIds = ec2ids
#     )
#     # print the ec2response...
#     print(ec2response)
