from django.contrib import admin
from .models import Image, Like, Tag, Comment, Follow, Post



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

from django.utils.html import format_html





class ImageInline(admin.TabularInline):
    model = Image
    extra = 1  # تعداد فرم‌های خالی برای افزودن تصویر جدید

    # اگر می‌خواهید فیلد user به صورت خودکار مقداردهی شود:
    readonly_fields = ('user',)


class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('user', 'caption', 'created_at')

admin.site.register(Post, PostAdmin)



admin.site.register(Like)    