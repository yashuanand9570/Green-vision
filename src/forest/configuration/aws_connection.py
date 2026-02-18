import boto3
import os
from dotenv import load_dotenv
load_dotenv()

class S3Client:

    s3_client=None
    s3_resource = None
    def __init__(self, region_name: str = None):

        # Keep local runs working even if AWS env vars are missing.
        if region_name is None:
            region_name = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

        if S3Client.s3_resource==None or S3Client.s3_client==None:
            __access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
            __secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

            # If explicit keys aren't provided, boto3 will use its default credential chain.
            if __access_key_id and __secret_access_key:
                S3Client.s3_resource = boto3.resource(
                    "s3",
                    aws_access_key_id=__access_key_id,
                    aws_secret_access_key=__secret_access_key,
                    region_name=region_name,
                )
                S3Client.s3_client = boto3.client(
                    "s3",
                    aws_access_key_id=__access_key_id,
                    aws_secret_access_key=__secret_access_key,
                    region_name=region_name,
                )
            else:
                S3Client.s3_resource = boto3.resource("s3", region_name=region_name)
                S3Client.s3_client = boto3.client("s3", region_name=region_name)
        self.s3_resource = S3Client.s3_resource
        self.s3_client = S3Client.s3_client

