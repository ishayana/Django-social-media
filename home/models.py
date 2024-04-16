from django.db import models

# Create your models here.

class BlogModel(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    created = models.DateField(auto_now=True)
    thumbnail = models.ImageField(upload_to='blog_image/')

    def blog_images(self):
        return self.images.all()
class BlogimageModel(models.Model):
    blog = models.ForeignKey(BlogModel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
