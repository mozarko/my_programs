from celery_config import celery_app
from domain.user_service import UserService

@celery_app.task
def register_user_task(login, password):
    return UserService().register(login, password)
