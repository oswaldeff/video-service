import uuid

from typing import List

from fastapi import UploadFile

from src.aws.dynamodb_client import DynamoDBClient
from src.aws.s3_client import S3Client
from src.api.upload.tasks import upload_video_task

class UploadService:
    def __init__(
            self,
            dynamodb_client: DynamoDBClient,
            s3_client: S3Client
        ):
        self.dynamodb_client = dynamodb_client
        self.s3_client = s3_client

    async def upload_videos(
            self,
            files: List[UploadFile]
        ) -> List[str]:
        video_ids = []
        for file in files:
            video_id = str(uuid.uuid4())
            video_ids.append(video_id)
            try:
                file_data = await file.read()
                path = "original"
                filename = file.filename
                content_type = file.content_type
                upload_video_task.delay(file_data, path, filename, content_type, self.dynamodb_client, self.s3_client)
            except Exception as e:
                raise e

        return video_ids
