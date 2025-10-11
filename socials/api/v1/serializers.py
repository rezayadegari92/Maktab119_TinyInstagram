from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from accounts.models import CustomUser
from socials.models import Like, Comment, Post, Image

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
        read_only = True
    )
    like_count = serializers.IntegerField(source="likes.count", read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'like_count', 'is_liked','created_at']

    @extend_schema_field(serializers.BooleanField)
    def get_is_liked(self, obj):
        if 'request' in self.context:
            user = self.context["request"].user
            return obj.likes.filter(user__username=user.username).exists()
        return False
    
class ImageSerializer(serializers.ModelSerializer):
    class Meta :
        model = Image
        fields = ['id', 'image', 'image_type','created_at']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username", 
        read_only=True
    )
    like_count = serializers.IntegerField(source="likes.count", read_only=True)
    is_liked = serializers.SerializerMethodField()
    likes = LikeSerializer(source="likes.all", many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    image_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    caption = serializers.CharField(allow_blank=True, required=False)
    
    class Meta:
        model = Post
        fields = ['id', 'user', 'images', 'caption', 'is_liked','comments', 'likes', 'like_count', 'created_at','image_files']

    @extend_schema_field(serializers.BooleanField)
    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user
            content_type = ContentType.objects.get_for_model(Post)
            return Like.objects.filter(user=user, content_type=content_type, object_id=obj.id).exists()
        return False
    
    def create(self, validated_data):
        # Extract image_files from validated data
        image_files = validated_data.pop('image_files', [])
        
        # Create the post
        post = Post.objects.create(**validated_data)
        
        # Create images
        for image_file in image_files:
            Image.objects.create(post=post, image=image_file)
        
        return post
    
    def update(self, instance, validated_data):
        # Extract image_files from validated data
        image_files = validated_data.pop('image_files', [])
        
        # Update post fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Replace images if new ones are provided
        if image_files:
            # Delete old images
            instance.images.all().delete()
            
            # Create new images
            for image_file in image_files:
                Image.objects.create(post=instance, image=image_file)
        
        return instance
