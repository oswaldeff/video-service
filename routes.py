from fastapi import APIRouter

from src.api.upload.routes import router as upload_router

router = APIRouter()
router.include_router(upload_router, tags=["upload"], prefix="/upload")
