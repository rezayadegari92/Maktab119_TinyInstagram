from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None  # Remove the username field
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=20)
    last_name = models.CharField(_("last name"), max_length=20)
    birth_date = models.DateField(_("birth date"))
    phone_number = models.CharField(_("phone number"), max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(_("profile picture"), upload_to='profile_pictures/', blank=True, null=True)

    USERNAME_FIELD = "email"  # Use email as the unique identifier
    REQUIRED_FIELDS = ["first_name", "last_name", "birth_date"]  # Add required fields

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")