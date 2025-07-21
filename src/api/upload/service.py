import uuid

from typing import Tuple, List

from fastapi import UploadFile
from celery.result import AsyncResult

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
        ) -> Tuple[List[str], List[str]]:
        video_ids = []
        task_ids = []

        for file in files:
            video_id = str(uuid.uuid4())
            video_ids.append(video_id)
            try:
                file_data = await file.read()
                author = "unknown"
                path = "original"
                filename = file.filename
                content_type = file.content_type
                
                task = upload_video_task.apply_async(
                    args=[video_id, author, file_data, path, filename, content_type]
                )
                task_ids.append(task.id)
            except Exception as e:
                raise e

        return video_ids, task_ids
    
    def check_task_results(self, task_ids: List[str]):
        for task_id in task_ids:
            result = AsyncResult(task_id)
            if result.failed():
                raise Exception(f"Task {task_id} failed: {result.info}")
