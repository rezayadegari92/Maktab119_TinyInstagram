from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize = value.size
    max_size = 5 * 1024 * 1024 
    if filesize > max_size :
        raise ValidationError("max size for upload is 5MB")

class CustomUser(AbstractUser):
    #add username 
    #indexing for username search it 
    username = models.CharField(
        _("username"),
        max_length=35,
        unique=True,
        db_index=True,
        help_text=_("Required. 150 characters or fewer. letters, digits and @/./+/-/_ only."),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=20)
    last_name = models.CharField(_("last name"), max_length=20)
    birth_date = models.DateField(_("birth date"))
    phone_number = models.CharField(_("phone number"), max_length=15, blank=True, null=True)
    USERNAME_FIELD = "email"  # Use email as the unique identifier
    REQUIRED_FIELDS = ["username","first_name", "last_name", "birth_date"]  # Add required fields

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")







class TimestampMixin(models.Model):
    """
    A mixin that adds `created_at` and `updated_at` fields to a model.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        abstract = True  # Ensures this mixin is not created as a separate database table        


class Profile(TimestampMixin):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=False, blank=False, related_name="profile")
    website = models.CharField(max_length=255, blank=True, null=True, default=None)
    #limited image must be added for validation 
    profile_picture = models.ImageField(_("profile picture"),
                                         upload_to='profile_pictures/', 
                                         blank=True, 
                                         null=True,
                                         validators=[validate_file_size],
                                         default=None
                                         )
    #limited image must be added for validation 
    
    bio = models.TextField(blank=True, null=True, default=None)
    location = models.CharField(max_length=100, blank=True, null=True, default=None)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile of {self.user.username}"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"



from django.utils import timezone
from django.core.mail import send_mail
import random


class Otp(models.Model):

    email = models.EmailField(_("email_address"),unique=True)
    otp_code = models.CharField(max_length=6)  # OTP codes are typically 4-6 digits
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta :
        unique_together = ("email", "otp_code")
        
    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))
    
    @classmethod
    def send_otp_email(cls,email):
        cls.objects.filter(email=email).delete()
        otp_code = cls.generate_otp()
        otp = cls.objects.create(email=email, otp_code= otp_code )
        send_mail(
            subject="Your otp code ",
            message=f"your otp code is : {otp_code} ",
            from_email="yadegarireza50@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )
        return otp_code
    def __str__(self):
        return f"OTP for {self.email}"