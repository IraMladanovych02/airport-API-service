from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(to_email):
    subject = "Welcome to Airport Service!"
    message = (
        "Hi there,\n\n"
        "Thanks for registering with us.\n"
        "We hope you enjoy using our service! ✈️\n\n"
        "Best regards,\n"
        "The Airport Team"
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        fail_silently=False,
    )
