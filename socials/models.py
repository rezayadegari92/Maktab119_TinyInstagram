from django.db import models
from accounts.models import TimestampMixin, CustomUser
# Create your models here.

class Image(TimestampMixin):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="images")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/')
    IMAGE_TYPE_CHOICES = (
        ('post','Post'),
        ('story','Story'),
        ('other','Other'),
    )
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPE_CHOICES, default='post')

    def __str__(self):
        return f"image is for {self.user.username}"
    
    def save(self, *args, **kwargs):
        self.user = self.post.user
        super().save(*args, **kwargs)


from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class Like(TimestampMixin):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', "content_type", "object_id")

    def __str__(self):
        return f"{self.user.username}liked  {self.content_type} on {self.object_id}"    

class Tag(models.Model):
    tag_name =  models.TextField(max_length=50, unique=True)
    def __str__(self):
        return self.tag_name

class Comment(TimestampMixin):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='comments')
    text = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    likes = GenericRelation(Like, related_query_name="comments")
    def __str__(self):
        return f"comment by {self.user.username} on post {self.post.id}"


class Follow(models.Model):
    owner =models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='following')
    followed_users = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='follower')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'followed_users')
    def __str__(self):
        return f":)"
    @staticmethod
    def get_followers(user):
        return user.follower.all()
    @staticmethod
    def get_followings(user):
        return user.following.all()

class Post(TimestampMixin):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    likes = GenericRelation(Like, related_query_name="posts")
    caption = models.TextField(blank=True, null=True)
    is_archive = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts') 
    location = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f"post by {self.user.username}"





