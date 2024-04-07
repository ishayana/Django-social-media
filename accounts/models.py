from django.db import models
from django.contrib.auth.models import User


class UserprofileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='accounts/avatars/', default='media/base/user_avatar.jpeg')


        