from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_email_task(subject,message,recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email= settings.EMAIL_HOST_USER,
        recipient_list=recipient_list
    )
    return None

