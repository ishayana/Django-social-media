from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .utils import Resize_image
import os


#Post model
class PostModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'posts')
    description = models.TextField(max_length=300)
    image = models.ImageField(null=True, blank=True, upload_to='')
    created = models.DateTimeField(auto_now_add=True)
    edit = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image: 
            Resize_image(self.image)

    def __str__(self):
        return self.description

    def get_absolut_url(self):
        return reverse('userprofile:post', args=[self.author.username, self.id])
    
    def get_author_username(self):
        return self.author.get_username
    

    def comments_counter(self):
        return self.postcomment.filter(is_reply=False).count()

    def like_counter(self):
        return self.likes.all().count()
    
    def user_like(self, user):
        return self.likes.filter(user=user, post_id=self).exists()

class FollowModel(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete= models.CASCADE, related_name="following")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower} followed {self.following}'
    
    
class CommentModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usercomment')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='postcomment')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replycomment', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    description = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.description}'
    
    def reply_counter(self):
        return CommentModel.objects.filter(reply=self, is_reply=True).count()

class LikeModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userliked')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{self.user} liked this post: {self.post}"