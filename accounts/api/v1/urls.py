from django.urls import path
from .views import UserRegistrationView, VerifyOtpView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
]
