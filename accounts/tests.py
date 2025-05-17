from django.test import TestCase

# Create your tests here.
from django.core.mail import send_mail

send_mail(
    subject="test email",
    message="this is me ",
    from_email="yadegarireza50@gmail.com",
    recipient_list=["yadegarireza50@yahoo.com"],
    fail_silently=False,
)