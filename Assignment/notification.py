from django.core.mail import send_mail
from SimpleUserManagement.settings import *
from django.template.loader import render_to_string

def send_email_notification(receiver=None,subject="please use this link for account activation",token=""):


    link="http://127.0.0.1:8000/user/activate/"+token

    send_mail(subject, link, EMAIL_HOST_USER,\
              [receiver,], fail_silently=False)
    return True