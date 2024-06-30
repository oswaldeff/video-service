from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from celery.result import AsyncResult

from src.settings.dispatch import create_settings
from src.aws.dynamodb_client import DynamoDBClient
from src.aws.s3_client import S3Client
from src.api.upload.service import UploadService

router = APIRouter()

@router.post("/videos")
async def upload_videos(
    files: List[UploadFile] = File(...),
    dynamodb_client: DynamoDBClient = Depends(lambda: DynamoDBClient(settings=create_settings())),
    s3_client: S3Client = Depends(lambda: S3Client(settings=create_settings()))
):
    try:
        service = UploadService(dynamodb_client, s3_client)
        video_ids, task_ids = await service.upload_videos(files)
        for task_id in task_ids:
            result = AsyncResult(task_id)
            result.get(timeout=10)
            if result.failed():
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Task {task_id} failed: {result.info}"
                )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"video_ids": video_ids}
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str("INTERNL SERVER ERROR")
        )
