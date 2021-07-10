#!/usr/bin/env python3
#
# Title: rds_changesgs.p.py
#
# Description: rds_createdbfromsnap.py uses the aws module, boto3, to make
# api calls to create a snapshot of a db identifier (rds db has to exist)
# and then use that snap to create an RDS instance
#
# Usage: rds_changesgs.py [original|new]
#
# Requirements
# - proper aws iam privs to do the work
# - python 3.7.x
# - pip installed
# - boto3 installed
#
################################################################################
# imports...
################################################################################
import boto3
import time
import argparse
import yaml
import smtplib
from datetime import datetime, timezone, timedelta, date
import os
import sys
################################################################################

# functions...
################################################################################
# def get_session(region):
#     return boto3.session.Session(region_name=region)


def dbinstance_origsgs():
    # add ec2 security groups to the clone...
    #rdsclient = boto3.client('rds')
    rdsresponse = rdsclient.modify_db_instance(
        DBInstanceIdentifier=params['DatabaseInstanceName'],
        VpcSecurityGroupIds=['sg-xxxxxxxx', 'sg-xxxxxxxx', 'sg-xxxxxxxx',
                             'sg-xxxxxxxxxxxxxxxxx', 'sg-xxxxxxxxxxxxxxxxx', 'sg-xxxxxxxxxxxxxxxxx']
    )


def dbinstance_newsgs():
    # add ec2 security groups to the clone...
    #rdsclient = boto3.client('rds')
    rdsresponse = rdsclient.modify_db_instance(
        DBInstanceIdentifier=params['DatabaseInstanceName'],
        VpcSecurityGroupIds=['sg-xxxxxxxxxxxxxxxxx']
    )

################################################################################


# main portion...
################################################################################
# parse the command line...
parser = argparse.ArgumentParser(description='Script to change the security groups of a database')
parser.add_argument('command', help='original or new', action='store', default='original')
args = parser.parse_args()

# connect to aws, rds as client...
rdsclient = boto3.client('rds')

# load yaml manifest to assign parameters...
# with open('test.manifest.yml') as manifest:
with open('/Users/xxxxxxxxxx/samba/code/python/aws/rds/changesgs-manifest.yml') as manifest:
    params = yaml.load(manifest, Loader=yaml.FullLoader)

# decision time...
if args.command == 'original':
    region = params['AwsRegion']
    output = params['AwsOutPut']
    dbinstance_origsgs()
else:
    region = params['AwsRegion']
    output = params['AwsOutPut']
    dbinstance_newsgs()
