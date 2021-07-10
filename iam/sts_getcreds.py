#!/usr/bin/env python3
#
# Title: sts_getcreds.py
#
# Description: sts_getcreds.py is used in tandem with okta_aws to populate a hidden text file
# so that the sts creds acquired from okta_aws can be exported as bash shell env variables.
# AWS CLI and Boto3 reference shell env variables first and then looks for creds in ~/.aws/credentials.
# sts_getcreds.py parses the ~/.aws/credentials file and breaks the creds out by account.
#
# Usage: sts_getcreds.py [ account profile ]
#        sts_getcreds.py -h for help
#
# Prereqs:
# - AWS CLI installed properly
# - Python 3. Preferrable >=3.7.2
# - Okta-based AWS role that can be assumed
# - okta_aws installed to assume an okta-based role and then populate the ~/.aws/credentials
#   file (https://github.com/chef/okta_aws)
#
###############################################
# imports
import boto3
import argparse
import os
import configparser
from configparser import RawConfigParser

# define the profile you want to work with
parser = argparse.ArgumentParser(description='Fetch the AWS account creds keys and tokens')
parser.add_argument('account', help='declare the AWS account as an argument, either sandbox, prod, or nonprod',
                    action='store', default='nonprod')
args = parser.parse_args()

# capture the account name
account = args.account

# initialize the aws keys and tokens
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_SESSION_TOKEN = ''

# get the creds file
path = os.path.join(os.path.expanduser('~'), '.aws/credentials')

# parse the creds file
config = RawConfigParser()
config.read(path)

# get values for the variables. key - value
AWS_ACCESS_KEY_ID = config.get(account, 'aws_access_key_id')
AWS_SECRET_ACCESS_KEY = config.get(account, 'aws_secret_access_key')
AWS_SESSION_TOKEN = config.get(account, 'aws_session_token')

# open a file to house the sts creds
stspath = os.path.join(os.path.expanduser('~'), '.sts'+account)
stsf = open(stspath, 'w')

# write the sts creds file for the account
print('export AWS_ACCESS_KEY_ID = ' + AWS_ACCESS_KEY_ID + '\n' + 'export AWS_SECRET_ACCESS_KEY = ' +
      AWS_SECRET_ACCESS_KEY + '\n' + 'export AWS_SESSION_TOKEN = ' + AWS_SESSION_TOKEN, file=stsf)

# close the file handle to the sts creds file
stsf.close()
