#!/usr/bin/env python3
#
# Title: rds_createadhocsnap.py
#
# Description: rds_createadhocnap.py uses the aws module, boto3, to make
# api calls to create a snapshot of a db identifier (has to exist) and then
# use that snap to create an RDS instance
#
# Usage: rds_createadhocsnap.py [create|delete]
#
# Requirements
# - proper aws iam privs to do the work
# - python 3.8.x
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


def get_session(region):
    return boto3.session.Session(region_name=region)


def create_snap():
    # connect to rds
    rdsclient = boto3.client('rds')

    # create the snapshot of the db id...
    rdsresponse = rdsclient.create_db_cluster_snapshot(
        DBClusterSnapshotIdentifier=params['DBClusterSnapshotIdentifier'],
        DBClusterIdentifier=params['DBClusterIdentifier'],
        Tags=[
            {
                'Key': 'Environment',
                'Value': 'PROD'
            },
            {
                'Key': 'Stack',
                'Value': 'Shared'
            },
        ]
    )
    dbsnap = rdsclient.describe_db_cluster_snapshots(
        DBClusterIdentifier=params['DBClusterIdentifier'],
        DBClusterSnapshotIdentifier=params['DBClusterSnapshotIdentifier'],
        SnapshotType='manual'
    )
    snapstatus = dbsnap['DBClusterSnapshots'][0]['Status']
    snaparn = dbsnap['DBClusterSnapshots'][0]['DBClusterSnapshotArn']
    while snapstatus != "available":
        snapresponse = rdsclient.describe_db_cluster_snapshots(
            DBClusterIdentifier=params['DBClusterIdentifier'],
            DBClusterSnapshotIdentifier=params['DBClusterSnapshotIdentifier'],
            SnapshotType='manual'
        )
        snapstatus = snapresponse['DBClusterSnapshots'][0]['Status']
        if snapstatus != "available":
            time.sleep(30)
            print("Creating...")
    else:
        print("Snapshot ready")

    return snaparn


def template_validate():
    # connect to cloudformation
    cfclient = boto3.client('cloudformation')
    with open(params['TemplateName'], 'r', encoding='utf8') as template:
        # validate the template
        cfresponse = cfclient.validate_template(
            TemplateBody=template.read()
        )
        try:
            iamcapabilities = cfresponse['Capabilities'][0]
        except KeyError as error:
            iamcapabilities = 'None'

        return iamcapabilities


def stack_create():
    # new cloudformation connection...
    cfclient = boto3.client('cloudformation')
    if iamcapabilities != "None":
        with open(params['TemplateName'], 'r', encoding='utf8') as template:
            # create the stack and deploy...
            cfresponse = cfclient.create_stack(
                StackName=params['StackName'],
                TemplateBody=template.read(),
                Capabilities=[
                    iamcapabilities
                ],
                OnFailure='ROLLBACK',
                Parameters=[
                    {
                        'ParameterKey': 'VpcId',
                        'ParameterValue': params['VpcId']
                    },
                    {
                        'ParameterKey': 'RdsKey',
                        'ParameterValue': params['RdsKey']
                    },
                    {
                        'ParameterKey': 'KmsKey',
                        'ParameterValue': params['KmsKey']
                    },
                    {
                        'ParameterKey': 'Environment',
                        'ParameterValue': params['Environment']
                    },
                    {
                        'ParameterKey': 'DBClusterParameterGroup',
                        'ParameterValue': params['DBClusterParameterGroup']
                    },
                    {
                        'ParameterKey': 'DBParameterGroupName',
                        'ParameterValue': params['DBParameterGroupName']
                    },
                    {
                        'ParameterKey': 'AurClusterName',
                        'ParameterValue': params['AurClusterName']
                    },
                    {
                        'ParameterKey': 'DBIdentifier',
                        'ParameterValue': params['DBIdentifier']
                    },
                    {
                        'ParameterKey': 'AurDbReplica0Name',
                        'ParameterValue': params['AurDbReplica0Name']
                    },
                    {
                        'ParameterKey': 'AurDbInstanceClass',
                        'ParameterValue': params['AurDbInstanceClass']
                    },
                    {
                        'ParameterKey': 'SecurityGroupId',
                        'ParameterValue': params['SecurityGroupId']
                    },
                    {
                        'ParameterKey': 'DBClusterSnapshotArn',
                        'ParameterValue': snaparn
                    },
                    {
                        'ParameterKey': 'DBClusterSnapshotIdentifier',
                        'ParameterValue': params['DBClusterSnapshotIdentifier']
                    },
                    {
                        'ParameterKey': 'DBClusterIdentifier',
                        'ParameterValue': params['DBClusterIdentifier']
                    },
                    {
                        'ParameterKey': 'SubnetGroupName',
                        'ParameterValue': params['SubnetGroupName']
                    }
                ]
            )
    else:
        with open(params['TemplateName'], 'r', encoding='utf8') as template:
            # create the stack and deploy...
            cfresponse = cfclient.create_stack(
                StackName=params['StackName'],
                TemplateBody=template.read(),
                OnFailure='ROLLBACK',
                Parameters=[
                    {
                        'ParameterKey': 'VpcId',
                        'ParameterValue': params['VpcId']
                    },
                    {
                        'ParameterKey': 'RdsKey',
                        'ParameterValue': params['RdsKey']
                    },
                    {
                        'ParameterKey': 'KmsKey',
                        'ParameterValue': params['KmsKey']
                    },
                    {
                        'ParameterKey': 'Environment',
                        'ParameterValue': params['Environment']
                    },
                    {
                        'ParameterKey': 'DBClusterParameterGroup',
                        'ParameterValue': params['DBClusterParameterGroup']
                    },
                    {
                        'ParameterKey': 'DBParameterGroupName',
                        'ParameterValue': params['DBParameterGroupName']
                    },
                    {
                        'ParameterKey': 'AurClusterName',
                        'ParameterValue': params['AurClusterName']
                    },
                    {
                        'ParameterKey': 'DBIdentifier',
                        'ParameterValue': params['DBIdentifier']
                    },
                    {
                        'ParameterKey': 'AurDbReplica0Name',
                        'ParameterValue': params['AurDbReplica0Name']
                    },
                    {
                        'ParameterKey': 'AurDbInstanceClass',
                        'ParameterValue': params['AurDbInstanceClass']
                    },
                    {
                        'ParameterKey': 'SecurityGroupId',
                        'ParameterValue': params['SecurityGroupId']
                    },
                    {
                        'ParameterKey': 'DBClusterSnapshotArn',
                        'ParameterValue': snaparn
                    },
                    {
                        'ParameterKey': 'DBClusterSnapshotIdentifier',
                        'ParameterValue': params['DBClusterSnapshotIdentifier']
                    },
                    {
                        'ParameterKey': 'DBClusterIdentifier',
                        'ParameterValue': params['DBClusterIdentifier']
                    },
                    {
                        'ParameterKey': 'SubnetGroupName',
                        'ParameterValue': params['SubnetGroupName']
                    }
                ]
            )


def stack_status():
    # how's the deployment going?
    cfclient = boto3.client('cloudformation')
    stackstatus = 'IN_PROGRESS'
    while stackstatus != 'CREATE_COMPLETE':
        cfresponse = cfclient.describe_stacks(
            StackName=params['StackName']
        )
        stackstatus = cfresponse['Stacks'][0]['StackStatus']
        # print(stackstatus)
        time.sleep(30)
        print(stackstatus)
    else:
        print("Clone ready...")


def dbinstance_endpoint():
    # get the clone's endpoint to mail out...
    rdsclient = boto3.client('rds')
    rdsresponse = rdsclient.describe_db_instances(
        # DBInstanceIdentifier = params['DatabaseInstanceName']
        DBInstanceIdentifier=params['DatabaseInstanceName']
    )
    endpoint = rdsresponse['DBInstances'][0]['Endpoint']['Address']
    return endpoint


def delete_stack():
    # connect to cloudformation and delete the stack...
    stackstatus = 'CREATE_COMPLETE'
    cfclient = boto3.client('cloudformation')
    cfresponse = cfclient.delete_stack(
        StackName=params['StackName']
    )
    while stackstatus != 'Deleted':
        try:
            cfresponse = cfclient.describe_stacks(StackName=params['StackName'])
            stackstatus = cfresponse['Stacks'][0]['StackStatus']
        except cfclient.exceptions.ClientError as error:
            stackstatus = 'Deleted'

        if stackstatus != 'Deleted':
            time.sleep(30)
    else:
        print(params['StackName'] + " deleted")


def delete_snap():
    # delete the snap used in the manifest...
    rdsclient = boto3.client('rds')
    rdsresponse = rdsclient.delete_db_cluster_snapshot(
        DBClusterSnapshotIdentifier=params['DBClusterSnapshotIdentifier'],
    )


def mail_response():
    text = dbinstance_endpoint() + ', is available for use'
    subject = 'clone created'
    smtp = smtplib.SMTP('dig MX somecompany.com', 25)
    sender = 'ec2-user@c7n02.somedomain.biz'
    receiver = ['someperson@somecompany.com',
                'someperson@somecompany.com', 'someperson@somecompany.com']
    message = 'Subject: {}\n\n{}'.format(subject, text)
    try:
        smtp.sendmail(sender, receiver, message)
        print("Email sent")
        smtp.quit()
    except smtplib.ConnectionRefusedError as e:
        print("Failed to connect to email server")


def mail_stack():
    text = params['StackName'] + ' has been deleted'
    subject = 'stack deleted'
    smtp = smtplib.SMTP('dig MX somecompany.com', 25)
    sender = 'root@c7n02.somedomain.biz'
    receiver = 'someperson@somecompany.com'
    message = 'Subject: {}\n\n{}'.format(subject, text)
    try:
        smtp.sendmail(sender, receiver, message)
        print("Email sent")
        smtp.quit()
    except smtplib.ConnectionRefusedError as e:
        print("Failed to connect to email server")

################################################################################


# main portion...
################################################################################
# parse the command line...
parser = argparse.ArgumentParser(description='Script to create or delete an RDS DB ')
parser.add_argument('command', help='create or delete', action='store', default='create')
args = parser.parse_args()

# load yaml manifest to assign parameters...
# with open('test.manifest.yml') as manifest:
with open('/Users/xxxxxxxxxx/xxxxx/code/python/aws/rds/nprod-migrate-manifest.yml') as manifest:
    params = yaml.load(manifest, Loader=yaml.FullLoader)

# print(params)
# decision time...
if args.command == 'create':
    region = params['AwsRegion']
    output = params['AwsOutPut']
    snaparn = create_snap()
    print(snaparn)
    iamcapabilities = template_validate()
    print(iamcapabilities)
    stack_create()
    stack_status()
    # # endpoint = dbinstance_endpoint()
    # mail_response()
else:
    region = params['AwsRegion']
    output = params['AwsOutPut']
    # delete_stack()
    # delete_snap()
    # mail_stack()
