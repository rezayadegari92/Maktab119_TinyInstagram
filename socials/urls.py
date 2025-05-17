from django.urls import path, include

from .views import posts

urlpatterns = [
    path('posts/', posts, name= 'posts' ),

]