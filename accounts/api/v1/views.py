from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import CustomUser, Otp
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import AllowAny
from django.utils import timezone

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        otp_code = Otp.send_otp_email(email)
        
        return Response({"detail": "OTP has been sent to your email"}, status=status.HTTP_200_OK)


class VerifyOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.models import Profile
from accounts.api.v1.serializers import ProfileSerializer
from django.shortcuts import get_object_or_404
class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user.profile
    

class UserProfileView(RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):    
        username = self.kwargs.get("username")
        user = get_object_or_404(CustomUser, username=username)
        if user == self.request.user :
            return user.profile 
        
        if user.profile.is_private:
            self.permission_denied(self.request, message="this profile is private")
            
        return user.profile


