#!/Users/xxxxxxxxxx/.pyenv/shims/python

import boto3

ec2client = boto3.client('ec2')
response = ec2client.describe_instances()

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        # print the dictionary...
        print(instance)
        # print the value of the key, InstanceId, from the dictionary
        print(instance["InstanceId"])
