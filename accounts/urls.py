from django.urls import path
from .views import register_page, home, login

urlpatterns = [
    path('',home, name='home ' ),
    path('register/', register_page, name='register'),
    path('login/', login, name='api')
]