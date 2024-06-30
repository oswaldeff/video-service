import uuid

from fastapi import Depends

from src.celery.config import celery_app
from src.aws.dynamodb_client import DynamoDBClient
from src.aws.s3_client import S3Client

@celery_app.task(bind=True)
def upload_video_task(
        self,
        file_data: bytes,
        path: str,
        filename: str,
        content_type: str,
        dynamodb_client: DynamoDBClient = Depends(),
        s3_client: S3Client = Depends()
    ) -> None:
    try:
        video_id = str(uuid.uuid4())
        author = ""
        s3_client.upload_file_from_data(file_data, video_id, path, content_type)
        
        metadata = {
            "path": path,
            "filename": filename,
            "content_type": content_type,
        }
        dynamodb_client.save_metadata(video_id, author, metadata)
    except Exception as e:
        self.retry(exc=e, countdown=30, max_retries=2)
        raise e
