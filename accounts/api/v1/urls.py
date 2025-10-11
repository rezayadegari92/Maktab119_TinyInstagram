from django.urls import path
from .views import (
    RegisterUserView,
    VerifyOtpView,
    ProfileView,
    UpdateProfileView,
    ProfileListView,
    ProfileDetailView,
    LoginView,
    CustomTokenRefreshView,
)

urlpatterns = [
    # Authentication with JWT
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('register/', RegisterUserView.as_view(), name='user-registration'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    
    # Profile Management
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profiles/<int:id>/', ProfileDetailView.as_view(), name='profile-detail'),
]
