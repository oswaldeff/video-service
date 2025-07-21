import boto3

class S3Client:
    def __init__(
            self,
            settings
        ):
        self.client = boto3.client(
            's3',
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_s3_access_key_id,
            aws_secret_access_key=settings.aws_s3_secret_access_key
        )
        self.bucket_name = settings.aws_s3_bucket_name

    def upload_file_from_data(
            self,
            file_data: bytes,
            video_id: str,
            path: str,
            content_type: str
        ) -> None:
        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=f'{path}/{video_id}',
                Body=file_data,
                ContentType=content_type
            )
        except Exception as e:
            raise e
