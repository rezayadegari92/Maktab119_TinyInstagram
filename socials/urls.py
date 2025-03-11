from django.urls import path

from .views import posts

urlpatterns = [
    path('socials/posts/', posts, name="posts")
]