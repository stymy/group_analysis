# Import packages
import sys
import os
import csv
import boto
import boto.s3.connection
from boto.s3.key import Key
import glob

def callback(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

_files = glob.glob(sys.argv[1])
# AWS account info
C = csv.reader(open('fcp-indi-keys.csv',"rb"))
aws_access_key_id = C.next()[0].split('AWSAccessKeyId=')[-1]
aws_secret_access_key = C.next()[0].split('AWSSecretKey=')[-1]

# Open s3 connection
cf = boto.s3.connection.OrdinaryCallingFormat()
s3conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key, 
                         calling_format=cf)
# Get s3 bucket, ours would be 'fcp-indi'
b = s3conn.get_bucket('fcp-indi')

# Upload
# uploadfile = sys.argv[1]
#  print sys.argv[2]
#     destinationfile = os.path.join(sys.argv[2],sys.argv[1])
# else:
# destinationfile = os.path.join('',sys.argv[1])
for destinationfile in _files:
    print 'Checking  %s with FCP-INDI AWS-S3 Server' % \
        (destinationfile)
    k = b.new_key(destinationfile)
    if b.get_key(k) == None:
        print destinationfile "is not uploaded"
    if k.md5 != 
    else: print "already uploaded"
    print 'make public()'
    k.make_public()
    print 'done'
# k.get_contents_to_filename('./test.zip')
