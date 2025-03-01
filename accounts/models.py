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
    website = models.CharField(max_length=255, blank=True, null=True)
    #limited image must be added for validation 
    profile_picture = models.ImageField(_("profile picture"),
                                         upload_to='profile_pictures/', 
                                         blank=True, 
                                         null=True,
                                         validators=[validate_file_size]
                                         )
    #limited image must be added for validation 
    
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile of {self.user.email}"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"



from django.utils import timezone
from django.core.mail import send_mail
import random


class Otp(models.Model):
    email = models.EmailField(_("email_address"))
    otp_code = models.CharField(max_length=6)  # OTP codes are typically 4-6 digits
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # Add an expiration time for the OTP

    class Meta :
        unique_together = ("user", "otp_code")

    def __str__(self):
        return f"OTP for {self.email}"

    def is_expired(self):
        """Check if the OTP has expired."""
        return timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        """Set the expiration time when saving the OTP."""
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=5)  # OTP expires in 5 minutes
        super().save(*args, **kwargs)
    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))
    @classmethod
    def send_otp_email(cls,user):
        cls.objects.filter(user=user).delete()
        otp_code = cls.generate_otp()
        expiers_at = timezone.now() + timezone.timedelta(minutes=5)
        otp = cls.objects.create(user=user, )
        subject = "Your OTP Code"
        message = f"Your OTP code is: {otp_code}\nIt will expire in 5 minutes."
        send_mail(subject, message, "your_email@gmail.com", [email])
        return otp_code
    
    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"     