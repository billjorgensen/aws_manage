#!/Users/xxxxxxxxxx/.pyenv/shims/python
import boto3
import sys
import argparse

# parse the command line for positional arguments...
parser = argparse.ArgumentParser(description='Script to get contents of an S3 bucket')
parser.add_argument('BucketName', help='Name of the s3 bucket to list',
                    action="store", default='somecompany-development')
args = parser.parse_args()

# use boto3 client call: low-level access, exposes botocore, maps 1-1 with api
# service
client = boto3.client('s3')
response = client.list_objects(Bucket=args.BucketName)
# print(response)
for content in response['Contents']:
    obj_dict = client.get_object(Bucket=args.BucketName, Key=content['Key'])
    print(content['Key'], obj_dict['LastModified'])

# use boto3 resource call: object-oriented, uses identifiers and attributues
s3 = boto3.resource('s3')
bucket = s3.Bucket(args.BucketName)
for obj in bucket.objects.all():
    print(obj.key, obj.last_modified)
