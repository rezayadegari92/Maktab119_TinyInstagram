from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny

from socials.models import Post, Image, Comment, Follow
from accounts.models import CustomUser
from socials.services import PostService, LikeService, CommentService, FollowService
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .schemas import (
    post_list_schema,
    post_create_schema,
    post_detail_schema,
    post_update_schema,
    post_delete_schema,
    unlike_post_schema,
    comment_create_schema,
    comment_delete_schema
)


class PostListView(generics.ListAPIView):
    """List all posts from public profiles or followed private profiles"""
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        # Get visible posts using service
        queryset = PostService.get_visible_posts(user)

        # Apply filters
        tags = self.request.query_params.get('tags', None)
        location = self.request.query_params.get('location', None)

        if tags:
            queryset = queryset.filter(tags__tag_name=tags)
        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset.distinct().order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @post_list_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PostCreateView(APIView):
    """Create a new post with images"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = PostSerializer
    
    @post_create_schema
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # Serializer's create method will handle image creation
            post = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    """Get detailed information about a specific post"""
    permission_classes = [IsAuthenticated]
    
    @post_detail_schema
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        
        # Check if user can view this post
        if post.user.profile.is_private:
            if not Follow.objects.filter(owner=request.user, followed_users=post.user).exists():
                if post.user != request.user:
                    return Response(
                        {"error": "This post is from a private profile you don't follow"}, 
                        status=status.HTTP_403_FORBIDDEN
                    )
        
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostUpdateView(APIView):
    """Update a post (only owner can update) - Supports both PUT and PATCH with image uploads"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = PostSerializer
    
    @post_update_schema
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        
        # Check if user is the owner
        if post.user != request.user:
            return Response(
                {"error": "You do not have permission to update this post."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PostSerializer(post, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @post_update_schema
    def patch(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        
        # Check if user is the owner
        if post.user != request.user:
            return Response(
                {"error": "You do not have permission to update this post."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PostSerializer(post, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDeleteView(APIView):
    """Delete a post (only owner can delete)"""
    permission_classes = [IsAuthenticated]
    
    @post_delete_schema
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        
        # Check if user is the owner
        if post.user != request.user:
            return Response(
                {"error": "You do not have permission to delete this post."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        post.delete()
        return Response({"detail": "post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class LikePostView(APIView):
    """Like a post"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        
        # Check if user can interact with this post using service
        if not PostService.can_interact_with_post(request.user, post):
            return Response(
                {"error": "You cannot like posts from a private profile you don't follow"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if already liked using service
        if LikeService.is_liked_by_user(request.user, post):
            return Response({"detail": "you already like this :)"}, status=status.HTTP_200_OK)

        # Create like using service
        LikeService.toggle_like(request.user, post)
        return Response({"detail": "post liked :)"}, status=status.HTTP_201_CREATED)


class UnlikePostView(APIView):
    """Remove like from a post"""
    permission_classes = [IsAuthenticated]
    
    @unlike_post_schema
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        # Check if user liked the post using service
        if not LikeService.is_liked_by_user(request.user, post):
            return Response({"error": "You haven't liked this post"}, status=status.HTTP_404_NOT_FOUND)

        # Toggle like using service (this will remove the like)
        LikeService.toggle_like(request.user, post)
        return Response({"detail": "like removed :)"}, status=status.HTTP_200_OK)


class CommentCreateView(APIView):
    """Add a comment to a post"""
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, FormParser]
    serializer_class = CommentSerializer
    
    @comment_create_schema
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        # Check if user can interact with this post using service
        if not PostService.can_interact_with_post(request.user, post):
            return Response(
                {"error": "You cannot comment on posts from a private profile you don't follow"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            # Create comment using service
            comment = CommentService.create_comment(request.user, post, serializer.validated_data['text'])
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteView(APIView):
    """Delete a comment (only owner can delete)"""
    permission_classes = [IsAuthenticated]
    
    @comment_delete_schema
    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        
        # Check if user is the owner
        if comment.user != request.user:
            return Response(
                {"error": "You do not have permission to delete this comment."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        comment.delete()
        return Response({"detail": "comment deleted :)"}, status=status.HTTP_200_OK)


class FollowUserView(APIView):
    """Follow a user"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        
        # Can't follow yourself
        if user_to_follow == request.user:
            return Response(
                {"error": "You cannot follow yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if already following using service
        if FollowService.is_following(request.user, user_to_follow):
            return Response(
                {"detail": "you already follow this user"},
                status=status.HTTP_200_OK
            )

        # Follow user using service
        FollowService.toggle_follow(request.user, user_to_follow)
        return Response(
            {"detail": "user followed successfully"},
            status=status.HTTP_201_CREATED
        )


class UnfollowUserView(APIView):
    """Unfollow a user"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)

        # Check if following using service
        if not FollowService.is_following(request.user, user_to_unfollow):
            return Response(
                {"error": "You are not following this user"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Unfollow user using service
        FollowService.toggle_follow(request.user, user_to_unfollow)
        return Response(
            {"detail": "user unfollowed successfully"},
            status=status.HTTP_200_OK
        )


class FollowersListView(APIView):
    """Get list of followers for a user"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        followers = FollowService.get_followers(user)
        
        followers_data = [
            {
                'id': follow.owner.id,
                'username': follow.owner.username,
                'email': follow.owner.email
            }
            for follow in followers
        ]
        
        return Response(followers_data, status=status.HTTP_200_OK)


class FollowingListView(APIView):
    """Get list of users that a user is following"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        following = FollowService.get_following(user)
        
        following_data = [
            {
                'id': follow.followed_users.id,
                'username': follow.followed_users.username,
                'email': follow.followed_users.email
            }
            for follow in following
        ]
        
        return Response(following_data, status=status.HTTP_200_OK)
