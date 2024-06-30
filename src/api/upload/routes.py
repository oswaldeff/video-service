from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse

from src.aws.dynamodb_client import DynamoDBClient
from src.aws.s3_client import S3Client
from src.api.upload.service import UploadService

router = APIRouter()

@router.post("/videos")
async def upload_videos(
    files: List[UploadFile] = File(...),
    dynamodb_client: DynamoDBClient = Depends(),
    s3_client: S3Client = Depends()
):
    try:
        service = UploadService(dynamodb_client, s3_client)
        video_ids = await service.upload_videos(files)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"video_ids": video_ids}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
