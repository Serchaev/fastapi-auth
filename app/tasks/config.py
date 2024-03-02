from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://redis_db:6379",
    include=["app.tasks.tasks"],
)
