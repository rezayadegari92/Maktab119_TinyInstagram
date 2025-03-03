from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Otp
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