from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from account.tasks import send_welcome_email_task

@receiver(post_save, sender=User)
def send_welcome_email_on_user_creation(sender, instance, created, **kwargs):
    if created:
        send_welcome_email_task.apply_async(args=[instance.email], countdown=10)  # Set the delay in seconds (1 hour)
