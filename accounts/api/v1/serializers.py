
from wsgiref import validate
from rest_framework import serializers
from accounts.models import CustomUser, Otp, Profile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style = {'input_type': 'password'},validators=[validate_password])
    otp_code = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username','password', 'first_name', 'last_name', 'birth_date', 'phone_number', 'otp_code']
    
    def validate_otp_code(self, value):
        email = self.initial_data['email']
        otp = Otp.objects.filter(email=email).last()
        if not otp or otp.otp_code != value:
            raise ValidationError("Invalid OTP Code or OTP expired.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data["username"],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            birth_date=validated_data['birth_date'],
            phone_number=validated_data.get('phone_number', None)
        )
        
        # Skip Profile creation for now if user skips it
        Profile.objects.create(user=user)  # Can be skipped if needed
        
        return user
    

# class UserDetailSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, requierd = True, style = {'input_type':'password'})

#     class Meta :
#         model = CustomUser
#         fields = ['id','email', 'username','password', 'first_name', 'last_name', 'birth_date', 'phone_number', 'otp_code']


class ProfileSerializer(serializers.ModelSerializer):
    username = user = serializers.SlugRelatedField(
        slug_field="username", 
        queryset=CustomUser.objects.all()
    )
    post_images = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['id','username','website','bio','profile_picture', 'location','is_private','post_images']

    def get_post_images(self, obj):
        posts = obj.user.posts.all().order_by("-created_at")
        return [post.image.url for post in posts if post.image ]    