from celery_config import celery_app
import app

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)
