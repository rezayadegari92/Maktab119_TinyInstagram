"""
Services layer for accounts app - following SOLID principles
"""
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Otp, Profile


class UserService:
    """Service class for user operations"""

    @staticmethod
    def create_user(email, username, password, first_name, last_name, birth_date, phone_number=None):
        """Create a new user with profile"""
        user = CustomUser.objects.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            phone_number=phone_number
        )

        # Create profile
        Profile.objects.create(user=user)

        return user

    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user credentials"""
        return authenticate(username=email, password=password)

    @staticmethod
    def generate_jwt_tokens(user):
        """Generate JWT tokens for user"""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class OtpService:
    """Service class for OTP operations"""

    @staticmethod
    def send_otp_email(email):
        """Send OTP to email and return the code"""
        from django.core.mail import send_mail
        from django.conf import settings
        
        # Clean up existing OTPs for this email
        Otp.objects.filter(email=email).delete()

        # Generate and save new OTP
        otp_code = Otp.generate_otp()
        Otp.objects.create(email=email, otp_code=otp_code)

        # Send OTP via email (uses console backend in DEBUG mode)
        try:
            send_mail(
                subject="Your OTP Code - Tiny Instagram",
                message=f"Your OTP code is: {otp_code}\n\nThis code will expire in 5 minutes.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            # In development with console backend, this is normal
            # OTP will be printed to console
            print(f"📧 OTP Email (Console Backend): {otp_code}")
            print(f"   To: {email}")
        
        return otp_code

    @staticmethod
    def verify_otp(email, otp_code):
        """Verify OTP code"""
        otp = Otp.objects.filter(email=email, otp_code=otp_code).last()
        if otp and not otp.is_expired():
            otp.delete()  # One-time use
            return True
        return False


class ProfileService:
    """Service class for profile operations"""

    @staticmethod
    def can_view_profile(viewer, profile_owner):
        """Check if viewer can see the profile"""
        if profile_owner == viewer:
            return True  # Owner can always see their own profile

        if not profile_owner.profile.is_private:
            return True  # Public profiles are visible to all

        # Check if viewer follows the profile owner
        from socials.models import Follow
        return Follow.objects.filter(owner=viewer, followed_users=profile_owner).exists()
