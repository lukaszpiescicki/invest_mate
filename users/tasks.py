from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_email_task(mail_subject: str, message: str, to_email: str):
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
