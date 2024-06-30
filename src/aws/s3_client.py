import boto3

class S3Client:
    def __init__(self, settings):
        self.client = boto3.client(
            's3',
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_s3_access_key_id,
            aws_secret_access_key=settings.aws_s3_secret_access_key
        )
