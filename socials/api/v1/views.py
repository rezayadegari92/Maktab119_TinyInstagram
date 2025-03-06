from rest_framework import viewsets, permissions
from socials.models import Post
from socials.api.v1.serializers import PostSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]