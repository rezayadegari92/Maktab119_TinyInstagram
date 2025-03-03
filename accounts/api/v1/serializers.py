from rest_framework import serializers
from accounts.models import CustomUser, Otp, Profile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    otp_code = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name', 'birth_date', 'phone_number', 'otp_code')
    
    def validate_otp_code(self, value):
        email = self.initial_data['email']
        otp = Otp.objects.filter(email=email).last()
        if not otp or otp.otp_code != value:
            raise ValidationError("Invalid OTP Code or OTP expired.")
        if otp.is_expired():
            raise ValidationError("OTP has expired.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            birth_date=validated_data['birth_date'],
            phone_number=validated_data.get('phone_number', None)
        )
        
        # Skip Profile creation for now if user skips it
        Profile.objects.create(user=user)  # Can be skipped if needed
        
        return user