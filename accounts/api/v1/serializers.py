
from wsgiref import validate
from rest_framework import serializers
from accounts.models import CustomUser, Otp, Profile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, style = {'input_type': 'password'},validators=[validate_password])
#     otp_code = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = CustomUser
#         fields = ['email', 'username','password', 'first_name', 'last_name', 'birth_date', 'phone_number', 'otp_code']
    
#     def validate_otp_code(self, value):
#         email = self.initial_data['email']
#         otp = Otp.objects.filter(email=email).last()
#         if not otp or otp.otp_code != value:
#             raise ValidationError("Invalid OTP Code or OTP expired.")
#         return value

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(
#             email=validated_data['email'],
#             username=validated_data["username"],
#             password=validated_data['password'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             birth_date=validated_data['birth_date'],
#             phone_number=validated_data.get('phone_number', None)
#         )
        
#         # Skip Profile creation for now if user skips it
#         Profile.objects.create(user=user)  # Can be skipped if needed
        
#         return user
    
from rest_framework import serializers
from accounts.models import CustomUser, Otp, Profile

class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text='Enter your email address for registration')
    username = serializers.CharField(help_text='Choose a unique username (3-35 characters)')
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, help_text='Create a strong password (min 8 characters)')
    first_name = serializers.CharField(help_text='Enter your first name')
    last_name = serializers.CharField(help_text='Enter your last name')
    birth_date = serializers.DateField(help_text='Enter your birth date (YYYY-MM-DD)')
    phone_number = serializers.CharField(required=False, help_text='Enter your phone number (optional)')

class OtpVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text='Enter the email address you used during registration')
    otp_code = serializers.CharField(help_text='Enter the 6-digit OTP code from your email')

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text='Enter your registered email address')
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, help_text='Enter your account password')

class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text='Enter the refresh token obtained from login')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'birth_date', 'phone_number']
        read_only_fields = ['id']

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['website', 'profile_picture', 'bio', 'location', 'is_private']
# class UserDetailSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, requierd = True, style = {'input_type':'password'})

#     class Meta :
#         model = CustomUser
#         fields = ['id','email', 'username','password', 'first_name', 'last_name', 'birth_date', 'phone_number', 'otp_code']


class ProfileListSerializer(serializers.ModelSerializer):
    """Serializer for profile list view - excludes posts for better performance"""
    user = serializers.SlugRelatedField(
        slug_field="username", 
        read_only = True
    )
    
    class Meta:
        model = Profile
        fields = ['id','user','website','bio','profile_picture', 'location','is_private']
        extra_kwargs = {
            'website': {'required': False},
            'bio': {'required': False},
            'location': {'required': False},
            'is_private': {'required': False},
            'profile_picture': {'required': False},
        }


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for profile detail view - includes posts"""
    user = serializers.SlugRelatedField(
        slug_field="username", 
        read_only = True
    )
    posts = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ['id','user','website','bio','profile_picture', 'location','is_private','posts']
        extra_kwargs = {
            'website': {'required': False},
            'bio': {'required': False},
            'location': {'required': False},
            'is_private': {'required': False},
            'profile_picture': {'required': False},
        }
    
    def get_posts(self, obj):
        from socials.api.v1.serializers import PostSerializer
        posts = obj.user.posts.all().order_by("-created_at")
        request = self.context.get('request')
        return PostSerializer(posts, many=True, context={'request': request}).data