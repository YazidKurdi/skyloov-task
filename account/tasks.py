from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_email_task(user_email):

    subject = 'Welcome to Skyloov'
    message = 'Thank you for joining Skyloov!'
    from_email = 'skyloov.assignment@gmail.com'
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)
