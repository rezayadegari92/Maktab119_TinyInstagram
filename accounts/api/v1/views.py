from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import CustomUser, Otp
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import AllowAny
from django.utils import timezone

# class UserRegistrationView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         email = request.data.get("email")
#         if not email:
#             return Response({"detail": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
#         otp_code = Otp.send_otp_email(email)
        
#         return Response({"detail": "OTP has been sent to your email"}, status=status.HTTP_200_OK)


# class VerifyOtpView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"detail": "User registered successfully!"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from accounts.models import CustomUser, Otp, Profile
from .serializers import UserRegistrationSerializer, OtpVerificationSerializer, ProfileSerializer

class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            # Send OTP
            otp_code = Otp.send_otp_email(email)
            return Response({"message": "OTP sent to your email.", "email": email}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOtpAndCompleteRegistrationView(APIView):
    def post(self, request):
        serializer = OtpVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            # Verify OTP
            otp = Otp.objects.filter(email=email, otp_code=otp_code).last()
            if not otp or otp.is_expired():
                return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
            # Create user
            user = CustomUser.objects.create_useruser = CustomUser.objects.create_user(
                email=email,
                username=request.data.get('username'),
                password=request.data.get('password'),
                first_name=request.data.get('first_name'),
                last_name=request.data.get('last_name'),
                birth_date=request.data.get('birth_date'),
                phone_number=request.data.get('phone_number')
            )
            # Create profile
            Profile.objects.create(user=user)
            return Response({"message": "Registration successful.", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ProfileView(APIView):
#     def get(self, request, user_id):
#         profile = Profile.objects.get(user_id=user_id)
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.models import Profile
from accounts.api.v1.serializers import ProfileSerializer
from django.shortcuts import get_object_or_404
# class ProfileView(RetrieveUpdateDestroyAPIView):
#     serializer_class = ProfileSerializer
#     permission_classes = [IsAuthenticated]
#     def get_object(self):
#         return self.request.user.profile
    

# class UserProfileView(RetrieveAPIView):
#     serializer_class = ProfileSerializer

#     def get_object(self):    
#         username = self.kwargs.get("username")
#         user = get_object_or_404(CustomUser, username=username)
#         if user == self.request.user :
#             return user.profile 
        
#         if user.profile.is_private:
#             self.permission_denied(self.request, message="this profile is private")

#         return user.profile

class ProfileView(APIView):
    def get(self, request, user_id):
        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            # Return a default profile if it doesn't exist
            profile = Profile(user_id=user_id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class UpdateProfileView(APIView):
    def post(self, request, user_id):
        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
