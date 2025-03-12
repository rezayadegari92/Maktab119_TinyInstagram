from django.urls import path, include

from .views import posts

urlpatterns = [
    path('socials/posts/', posts ),
    path('socials/posts/',include('socials.api.v1.urls')),

]