import boto3

class DynamoDBClient:
    def __init__(self, settings):
        self.client = boto3.client(
            'dynamodb',
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_dynamodb_access_key_id,
            aws_secret_access_key=settings.aws_dynamodb_secret_access_key
        )
