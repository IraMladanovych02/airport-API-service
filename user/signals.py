import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from notification.email_utils import send_welcome_email

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def send_email_on_user_created(sender, instance, created, **kwargs):
    if created:
        send_welcome_email(instance.email)
        logger.info(f"Email notification was sent successfully")
