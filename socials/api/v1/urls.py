from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import PostViewSet
from . import views
# router = DefaultRouter()
# router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    # path('', include(router.urls)),
    path('', views.PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('<int:post_id>/like/', views.LikePostView.as_view(), name='like-post'),
    path('<int:post_id>/comment/', views.CommentCreateView.as_view(), name='comment-post'),
    ]