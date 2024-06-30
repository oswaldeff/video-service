from typing import List

from pydantic_settings import BaseSettings

class AppBaseSettings(BaseSettings):
    app_name: str = "VideoApp"
    environment: str
    debug: bool
    allowed_hosts: List[str]
    allow_credentials: bool
    aws_region: str
    aws_s3_access_key_id: str
    aws_s3_secret_access_key: str
    aws_dynamodb_access_key_id: str
    aws_dynamodb_secret_access_key: str
