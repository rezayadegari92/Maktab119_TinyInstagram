from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListAPIView
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.services import UserService, OtpService, ProfileService
from accounts.models import CustomUser, Otp, Profile
from .serializers import (
    UserRegistrationSerializer,
    OtpVerificationSerializer,
    ProfileSerializer,
    ProfileListSerializer,
    LoginSerializer,
    UserSerializer,
    TokenRefreshSerializer
)
from .schemas import (
    register_user_schema,
    verify_otp_schema,
    profile_view_schema,
    update_profile_schema,
    profile_list_schema,
    profile_detail_schema,
    login_schema,
    token_refresh_schema,
)


class RegisterUserView(APIView):
    """Register a new user - Step 1: Send OTP and store user data in session"""
    permission_classes = [AllowAny]
    parser_classes = [FormParser, JSONParser]
    serializer_class = UserRegistrationSerializer
    
    @register_user_schema
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Store all validated data in session for later use
            validated_data = serializer.validated_data.copy()
            validated_data['birth_date'] = validated_data['birth_date'].isoformat()
            
            email = serializer.validated_data['email']
            
            # Save registration data to session
            request.session['registration_data'] = validated_data
            
            # Send OTP using service
            otp_code = OtpService.send_otp_email(email)
            return Response({
                "message": "OTP sent to your email.",
                "email": email
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpView(APIView):
    """Verify OTP code - Step 2: Verify OTP, create user, and return JWT tokens"""
    permission_classes = [AllowAny]
    parser_classes = [FormParser, JSONParser]
    serializer_class = OtpVerificationSerializer

    @verify_otp_schema
    def post(self, request):
        serializer = OtpVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']

            # Retrieve registration data from session
            registration_data = request.session.get('registration_data')
            if not registration_data:
                return Response({
                    "error": "Registration session expired. Please register again."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Verify OTP using service
            if not OtpService.verify_otp(email, otp_code):
                return Response({
                    "error": "Invalid or expired OTP."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check if user already exists
            if CustomUser.objects.filter(email=email).exists():
                return Response({
                    "error": "User with this email already exists."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Convert birth_date back to date object
            from datetime import datetime
            birth_date = datetime.strptime(
                registration_data['birth_date'], 
                "%Y-%m-%d"
            ).date()

            # Create user using service
            user = UserService.create_user(
                email=registration_data['email'],
                username=registration_data['username'],
                password=registration_data['password'],
                first_name=registration_data['first_name'],
                last_name=registration_data['last_name'],
                birth_date=birth_date,
                phone_number=registration_data.get('phone_number')
            )

            # Clear session data
            if 'registration_data' in request.session:
                del request.session['registration_data']

            # Generate JWT tokens using service
            tokens = UserService.generate_jwt_tokens(user)

            return Response({
                "message": "Registration successful.",
                "user": UserSerializer(user).data,
                "tokens": tokens
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Login and get JWT tokens"""
    permission_classes = [AllowAny]
    parser_classes = [FormParser, JSONParser]
    serializer_class = LoginSerializer
    
    @login_schema
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Authenticate user using service
            user = UserService.authenticate_user(email, password)

            if user is not None:
                # Generate JWT tokens using service
                tokens = UserService.generate_jwt_tokens(user)

                return Response(tokens, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Invalid email or password'
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    """Custom token refresh view with proper schema"""
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshSerializer

    @token_refresh_schema
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProfileView(APIView):
    """Get authenticated user's profile"""
    permission_classes = [IsAuthenticated] 
    
    @profile_view_schema
    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({
                "error": "Profile not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileView(APIView):
    """Update authenticated user's profile"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    @update_profile_schema
    def post(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({
                "error": "Profile not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully.",
                "profile": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @update_profile_schema
    def patch(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({
                "error": "Profile not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully.",
                "profile": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileListView(ListAPIView):
    """List and search profiles - excludes posts data for better performance"""
    queryset = Profile.objects.all() 
    serializer_class = ProfileListSerializer 
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username',]
    
    @profile_list_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProfileDetailView(RetrieveAPIView):
    """Get profile details by profile ID"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'id'
    
    @profile_detail_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
