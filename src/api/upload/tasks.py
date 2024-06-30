from src.celery.config import celery_app
from src.settings.dispatch import create_settings
from src.aws.dynamodb_client import DynamoDBClient
from src.aws.s3_client import S3Client

@celery_app.task(bind=True)
def upload_video_task(
        self,
        video_id: str,
        author: str,
        file_data: bytes,
        path: str,
        filename: str,
        content_type: str
    ) -> None:
    try:
        dynamodb_client = DynamoDBClient(settings=create_settings())
        s3_client = S3Client(settings=create_settings())

        s3_client.upload_file_from_data(file_data, video_id, path, content_type)
        metadata = {
            "path": path,
            "filename": filename,
            "content_type": content_type,
        }
        dynamodb_client.save_metadata(video_id, author, metadata)
    except Exception as e:
        # FIXME: rollback
        raise e
