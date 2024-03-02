import smtplib

from app.core import settings
from app.tasks.config import celery_app


@celery_app.task
def activate_account(email: str, link: str):
    message = f"Подтверждение аккаунта - {link}"
    sender = settings.SMTP_EMAIL
    password = settings.SMTP_PASS

    server = smtplib.SMTP(host=settings.SMTP_HOST, port=587)
    server.starttls()

    server.login(user=sender, password=password)
    server.sendmail(from_addr=server, to_addrs=email, msg=message)
