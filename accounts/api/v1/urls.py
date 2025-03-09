from django.urls import path
from .views import UserProfileView, UserRegistrationView, VerifyOtpView , ProfileView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('profile/', ProfileView.as_view(), name='my-profile'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),


]
