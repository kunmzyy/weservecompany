import boto3
import redshift_connector as rdc

region= 'eu-west-2'
bucket_name= 'olu-weserve'

s3_path='s3://{}/{}.csv'

access_key = 'AKIA2JVK4EED4UIH35QD'
secret_key = '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'

def create_s3_bucket():
    try:
        client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': region
            }
        )
        print('Bucket Created in S3lake')
    except Exception as error:
        print('Creation failed or Bucket exists')



def connect_to_dwh(conn_details):
    return rdc.connect(**conn_details)