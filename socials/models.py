from django.db import models
from accounts.models import TimestampMixin, CustomUser
# Create your models here.

class Image(TimestampMixin):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='posts/')
    IMAGE_TYPE_CHOICES = (
        ('post','Post'),
        ('story','Story'),
        ('other','Other'),
    )
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPE_CHOICES, default='post')

    def __str__(self):
        return f"image is for {self.user.username}"

class Like():
    like_status = models.BooleanField(default=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='likes')
    post = models.ForeignKey('Post', on_delete=models.CASCADE,related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"liked by {self.user.username} on post {self.post.id}"    

class Tag:
    tag_name =  models.TextField(max_length=50, unique=True)
    def __str__(self):
        return self.tag_name

class Comment(TimestampMixin):
    _user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='comments')
    text = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"comment by {self._user.username} on post {self.post.id}"


class Follow:
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
    Image = models.ForeignKey(Image,on_delete=models.CASCADE, null=True, blank=True, related_name='posts')

    caption = models.TextField(blank=True, null=True)
    is_archive = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, on_delete=models.CASCADE, blank=True, related_name='posts') 
    location = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f"post {self.id} by {self.user.username}"





