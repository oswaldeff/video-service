from celery import Celery
from src.settings.dispatch import create_settings

settings = create_settings()

celery_app = Celery(
    __name__,
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend
)
celery_app.conf.update(settings.model_dump())
