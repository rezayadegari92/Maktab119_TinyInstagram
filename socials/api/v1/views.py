from rest_framework import viewsets, permissions
from socials.models import Post
from socials.api.v1.serializers import PostSerializer


from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from socials.models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.permissions import IsAuthenticated

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if post.likes.filter(user=user).exists():
            post.likes.filter(user=user).delete()
        else:
            Like.objects.create(post=post, user=user)
        
        post.save()

        return Response({
            'likes': post.likes.count(),
            'is_liked': post.likes.filter(user=user).exists()
        })


    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        post = self.get_object()
        comment_text = request.data.get('text')

        comment = Comment.objects.create(post=post, user=request.user, text=comment_text)
        return Response(CommentSerializer(comment).data)