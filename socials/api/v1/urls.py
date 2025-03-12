
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostCreateView, PostListView, LikePostView, CommentCreateView


urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', PostCreateView.as_view, name='post-create'),
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like_post'),
    path('posts/<int:post_id>/coment/', CommentCreateView.as_view(), name='comment_create'),
    ]