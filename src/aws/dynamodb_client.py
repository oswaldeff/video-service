import boto3

class DynamoDBClient:
    def __init__(
            self,
            settings
        ):
        self.client = boto3.client(
            'dynamodb',
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_dynamodb_access_key_id,
            aws_secret_access_key=settings.aws_dynamodb_secret_access_key
        )
        self.table_name = settings.aws_dynamodb_table_name

    def save_metadata(
            self,
            video_id: str,
            author: str,
            metadata: dict
        ) -> None:
        try:
            self.client.put_item(
                TableName=self.table_name,
                Item={
                    'video_id': {'S': video_id},
                    'author': {'S': author},
                    'path': {'S': metadata['path']},
                    'filename': {'S': metadata['filename']},
                    'content_type': {'S': metadata['content_type']}
                }
            )
        except Exception as e:
            raise e
