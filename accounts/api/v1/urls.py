from django.urls import path
from .views import  RegisterUserView, VerifyOtpAndCompleteRegistrationView, ProfileView, UpdateProfileView, api_login

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='user-registration'),
    path('verify-otp/', VerifyOtpAndCompleteRegistrationView.as_view(), name='verify-otp'),
    # path('profile/', ProfileView.as_view(), name='profile'),
    # path('profile/<user_id>/', ProfileView.as_view(), name='user-profile'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('update-profile/<int:user_id>/', UpdateProfileView.as_view(), name='update-profile'),
    path('', api_login, name='api_login'),

]
