from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery import Celery
from django.core.mail import EmailMessage


@shared_task
def send_email_task(by, to):
    email_to = to
    email_subject = 'Thanks for using considereing me'
    email_body = 'Hi sir!,\nThanks for considereing me for this job post.\nHoping I get selected, I am really looking forward in contributin towards Fast App growth.\n Regards '+by
    email = EmailMessage(email_subject, email_body, to=[email_to])
    try :
        email.send()
        print('Email sent')
    except :
        print("Failed to send mail")
    return None