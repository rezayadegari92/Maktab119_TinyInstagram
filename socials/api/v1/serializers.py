

from django.forms import SlugField
from socials.models import *
from rest_framework import serializers


from rest_framework import serializers
from accounts.models import CustomUser
from socials.models import Like, Comment, Post

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username", 
        queryset=CustomUser.objects.all()
    )
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username", 
        queryset=CustomUser.objects.all()
    )
    like_count = serializers.IntegerField(source="likes.count", read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'like_count', 'created_at']
    
class ImageSerializer(serializers.ModelSerializer):
    class Meta :
        model = Image
        fields = ['id', 'image', 'image_type','created_at']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username", 
        queryset=CustomUser.objects.all()
    )
    like_count = serializers.IntegerField(source="likes.count", read_only=True)
    is_liked = serializers.SerializerMethodField()
    likes = LikeSerializer(source="likes.all", many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'images', 'caption', 'is_liked','comments', 'likes', 'like_count', 'created_at']

    def get_is_liked(self, obj):
        user = self.context["request"].user
        return obj.likes.filter(user__username=user.username).exists()