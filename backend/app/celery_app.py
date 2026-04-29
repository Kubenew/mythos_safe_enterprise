from celery import Celery
from app.config import settings

celery = Celery("mythos_safe", broker=settings.REDIS_URL, backend=settings.REDIS_URL)
