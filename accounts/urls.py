from django.urls import path
from .views import register_page, home, login, logout_view, profilesview

urlpatterns = [
    path('',home, name='home' ),
    path('register/', register_page, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profiles/', profilesview ,name='profiles'),
]