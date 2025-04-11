from django.core.mail import send_mail
from django.conf import settings
from .models import Notification


def send_email_to_artist(username, password, email):
    subject = "Welcome to Lumiere"
    message = (
        f"Dear {username},\n\n"
        f"Welcome to our platform! Your account has been created successfully.\n\n"
        f"Here are your credentials:\n"
        f"Username: {username}\n"
        f"Password: {password}\n\n"
        f"Please log in at your earliest convenience.\n\n"
        f"Best regards,\n"
        f"The Team"
    )
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,  # Set to False to raise an error if email fails to send
    )

def send_email_to_artist_update(username, password, email):
    subject = "Welcome to Lumiere"
    message = (
        f"Dear {username},\n\n"
        f"Welcome to our platform! Your account has been updated successfully.\n\n"
        f"Here are your credentials:\n"
        f"Username: {username}\n"
        f"Password: {password}\n\n"
        f"Please log in at your earliest convenience.\n\n"
        f"Best regards,\n"
        f"The Team"
    )
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,  # Set to False to raise an error if email fails to send
    )

def create_notification(artist, message):
    Notification.objects.create(artist=artist, message=message)