"""
Services layer for socials app - following SOLID principles
"""
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Post, Like, Comment, Follow, Image


class PostService:
    """Service class for post operations"""

    @staticmethod
    def get_visible_posts(user):
        """Get posts visible to a user (public + followed private)"""
        # Get users that the current user follows
        following_users = Follow.objects.filter(owner=user).values_list('followed_users', flat=True)

        # Get posts from public profiles or from users that current user follows
        posts = Post.objects.filter(
            user__profile__is_private=False
        ) | Post.objects.filter(
            user__id__in=following_users
        )

        return posts.distinct().order_by('-created_at')

    @staticmethod
    def can_interact_with_post(user, post):
        """Check if user can interact with a post (like, comment)"""
        if post.user == user:
            return True  # Owner can always interact

        if not post.user.profile.is_private:
            return True  # Public posts are open to all

        # Check if user follows the post owner
        return Follow.objects.filter(owner=user, followed_users=post.user).exists()

    @staticmethod
    def create_post(user, caption, location, images_data):
        """Create a post with images"""
        post = Post.objects.create(
            user=user,
            caption=caption,
            location=location
        )

        # Create images
        for image_data in images_data:
            Image.objects.create(post=post, image=image_data)

        return post


class LikeService:
    """Service class for like operations"""

    @staticmethod
    def toggle_like(user, post):
        """Toggle like on a post"""
        content_type = ContentType.objects.get_for_model(Post)
        like, created = Like.objects.get_or_create(
            user=user,
            content_type=content_type,
            object_id=post.id
        )

        if not created:
            like.delete()
            return False  # Unliked
        return True  # Liked

    @staticmethod
    def is_liked_by_user(user, post):
        """Check if post is liked by user"""
        content_type = ContentType.objects.get_for_model(Post)
        return Like.objects.filter(
            user=user,
            content_type=content_type,
            object_id=post.id
        ).exists()


class CommentService:
    """Service class for comment operations"""

    @staticmethod
    def create_comment(user, post, text):
        """Create a comment on a post"""
        return Comment.objects.create(
            user=user,
            post=post,
            text=text
        )


class FollowService:
    """Service class for follow operations"""

    @staticmethod
    def toggle_follow(follower, following):
        """Toggle follow relationship"""
        if follower == following:
            return False  # Can't follow yourself

        follow, created = Follow.objects.get_or_create(
            owner=follower,
            followed_users=following
        )

        if not created:
            follow.delete()
            return False  # Unfollowed
        return True  # Followed

    @staticmethod
    def is_following(follower, following):
        """Check if user follows another user"""
        return Follow.objects.filter(
            owner=follower,
            followed_users=following
        ).exists()

    @staticmethod
    def get_followers(user):
        """Get list of users following this user"""
        return Follow.objects.filter(followed_users=user).select_related('owner')

    @staticmethod
    def get_following(user):
        """Get list of users this user is following"""
        return Follow.objects.filter(owner=user).select_related('followed_users')
