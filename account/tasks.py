from celery import shared_task
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()
@shared_task
def send_welcome_email_task(user_id):

    user = User.objects.get(pk=user_id)
    token = default_token_generator.make_token(user)

    activation_link = f'http://127.0.0.1:8000/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{token}/'

    subject = 'Welcome to Skyloov'
    message = f'Thank you for joining Skyloov! Click the link below to activate your account:\n\n{activation_link}'
    from_email = 'skyloov.assignment@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
