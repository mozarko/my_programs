# celery_config.py
from celery import Celery
import os

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery(
    "xo_proj",
    broker=redis_url,
    backend=redis_url,
    include=["tasks"]  # 👈 тут указывается модуль с задачами
)

# celery_app = Celery(
#     "xo_proj",
#     broker="redis://localhost:6379/0",
#     backend="redis://localhost:6379/0",
#     include=["tasks"]  # 👈 тут указывается модуль с задачами
# )
