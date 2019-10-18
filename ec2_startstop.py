#!/Users/wjorgensen/.pyenv/shims/python
#
# Title: ec2_startstop.py
#
# Description: ec2_startstop.py sources a yaml file (ec2_ids.yml) with a list of ec2 instance
# ids. it uses a boto3 api call to either start or stop the list of ec2 ids...
#
# Example ec2_ids.yml
# ---
# # prod instances
# - i-xxxxxxxxxxxxxxxx
# - i-xxxxxxxxxxxxxxxx
# - i-xxxxxxxxxxxxxxxx
# - i-xxxxxxxxxxxxxxxx
#
# Usage: ec2_startstop.py [start|stop]
#
# Prerequisites:
# - python 3.7.x
# - boto3
# - appropriate aws iam privs to stop and start ec2 instances
# - pip installed
# - pyyaml installed
#
################################################################################
# imports...
import boto3
import yaml
import argparse

# get the command line argument...
parser = argparse.ArgumentParser(description='Script to stop or start EC2 instance ids in the yaml file ec2_ids.yml')
parser.add_argument('startstop', help='use start or stop as the argument', action='store', default='start')
args = parser.parse_args()

# load the list of instance ids...
with open('ec2_ids.yml') as manifest:
    ec2ids = yaml.load(manifest, Loader=yaml.FullLoader)

# start or stop...
if args.startstop == "start":
    client = boto3.client('ec2')
    response = client.start_instances(
        InstanceIds = ec2ids
    )
    # print the response...
    print(response)
else:
    client = boto3.client('ec2')
    response = client.stop_instances(
        InstanceIds = ec2ids
    )
    # print the response...
    print(response)
