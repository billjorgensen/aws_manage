#!/Users/xxxxxxxxxx/.pyenv/shims/python
import boto3
import datetime
# from dateutil import parser
from dateutil.tz import *
from dateutil.parser import *
import argparse

# parse the command line for positional arguments...
parser = argparse.ArgumentParser(
    description='Script to get Instance IDs with specific cost allocation tags')
parser.add_argument('DayDiff', help='Number of days from now, plus or minus',
                    action="store", default='Stack')
args = parser.parse_args()


client = boto3.client('ec2')
response = client.describe_instances()
print(args.DayDiff)

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        launchtime = instance["LaunchTime"]
        launchtime_naive = launchtime.replace(tzinfo=None)
        # then = datetime.datetime.utcnow() + datetime.timedelta(days=-30)
        then = datetime.datetime.utcnow() + datetime.timedelta(days=int(args.DayDiff))
        # print(launchtime_naive,then)
        # launched less than DayDiff if DayDiff is a negative number
        if launchtime_naive > then:
            # launched greeater than DayDiff if DayDiff is a negative number
            # if launchtime_naive < then:
            # print(instance["InstanceId"],launchtime_naive,then)
            print(instance["InstanceId"], launchtime_naive)
