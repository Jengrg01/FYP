from django.core.mail import send_mail
from django.conf import settings
from .models import Notification
#for email authentication a token will be generated as well with email
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string


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

#this is to provide notifs to artist
def create_notification(artist, message):
    Notification.objects.create(artist=artist, message=message)


#for user activation
def send_activation_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = request.build_absolute_uri(
        reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
    )

    subject = 'Activate your account'
    message = render_to_string('user/activation_email.html', {
        'user': user,
        'activation_link': activation_link
    })

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
