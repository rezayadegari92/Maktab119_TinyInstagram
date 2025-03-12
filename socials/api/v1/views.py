from email.mime import image
from rest_framework import viewsets, permissions
from socials.models import Post
from socials.api.v1.serializers import PostSerializer
from rest_framework import generics, permissions, status
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from socials.models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.permissions import IsAuthenticated

# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]

    
#     @action(detail=True, methods=['post'])
#     def like(self, request, pk=None):
#         post = self.get_object()
#         user = request.user

#         if post.likes.filter(user=user).exists():
#             post.likes.filter(user=user).delete()
#         else:
#             Like.objects.create(post=post, user=user)
        
#         post.save()

#         return Response({
#             'likes': post.likes.count(),
#             'is_liked': post.likes.filter(user=user).exists()
#         })


#     @action(detail=True, methods=['post'])
#     def comment(self, request, pk=None):
#         post = self.get_object()
#         comment_text = request.data.get('text')

#         comment = Comment.objects.create(post=post, user=request.user, text=comment_text)
#         return Response(CommentSerializer(comment).data)


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        # فیلتر کردن بر اساس تگ یا لوکیشن در صورت نیاز
        tags = self.request.query_params.get('tags', None)
        location = self.request.query_params.get('location', None)

        if tags:
            queryset = queryset.filter(tags__tag_name=tags)
        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from socials.models import Post, Image
from .serializers import PostSerializer


class PostCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        
        if serializer.is_valid():
            # پست جدید ذخیره می‌شود
            post = serializer.save(user=request.user)

            # اگر عکس‌ها ارسال شده‌اند، ذخیره می‌شوند
            images = request.data.get('images', [])
            for image_data in images:
                image = Image.objects.create(post=post, **image_data)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    


class CommentCreateView(APIView):
    def post(self, request, post_id) :
        post = Post.objects.get(id=post_id)
        serializer = CommentSerializer(data=request.data) 

        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

class LikePostView(APIView):
    def post(self, request, post_id) :
        post = Post.objects.get(id=post_id)
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({"detail":"you already like this :)"})
        like = Like.objects.create(user=request.user, post=post)  
        return Response({"detail":"post liked :)"}, status=status.HTTP_201_CREATED)
