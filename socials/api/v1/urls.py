from django.urls import path
from .views import (
    PostListView,
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    LikePostView,
    UnlikePostView,
    CommentCreateView,
    CommentDeleteView,
    FollowUserView,
    UnfollowUserView,
    FollowersListView,
    FollowingListView
)

urlpatterns = [
    # Post endpoints
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/update/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:post_id>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    # Like endpoints
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:post_id>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
    
    # Comment endpoints
    path('posts/<int:post_id>/comment/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    
    # Follow endpoints
    path('users/<int:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('users/<int:user_id>/unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('users/<int:user_id>/followers/', FollowersListView.as_view(), name='followers-list'),
    path('users/<int:user_id>/following/', FollowingListView.as_view(), name='following-list'),
]
