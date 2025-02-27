from django.contrib import admin
from .models import Image, Like, Tag, Comment, Follow, Post

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'image_type', 'created_at')
    list_filter = ('image_type', 'created_at')
    search_fields = ('user__username',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'like_status', 'created_at')
    search_fields = ('user__username', 'post__id')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_name',)
    search_fields = ('tag_name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__id', 'text')

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('owner', 'followed_users', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('owner__username', 'followed_users__username')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'Image', 'caption', 'is_archive', 'location', 'created_at')
    list_filter = ('is_archive', 'created_at')
    search_fields = ('user__username', 'caption', 'location')
    filter_horizontal = ('tags',)