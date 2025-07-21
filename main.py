import uvicorn

import sys

from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from celery import Celery

from src.settings.dispatch import create_settings
from src.aws.dynamodb_client import DynamoDBClient
from src.aws.s3_client import S3Client
from routes import router

def get_dynamodb_client(settings=Depends(create_settings)):
    return DynamoDBClient(settings=settings)

def get_s3_client(settings=Depends(create_settings)):
    return S3Client(settings=settings)

def create_app() -> FastAPI:
    settings = create_settings()
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=settings.allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # FIXME event handler

    # FIXME exeption handler

    app.include_router(
        router,
        dependencies=[Depends(get_dynamodb_client), Depends(get_s3_client)]
    )

    return app

app = create_app()

if __name__ == "__main__":
    if 'prod' in sys.argv:
        uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=False)
    else:
        uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
