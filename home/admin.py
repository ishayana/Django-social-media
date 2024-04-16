from django.contrib import admin
from .models import BlogModel, BlogimageModel
# Register your models here.



class BioInline(admin.TabularInline):
    model = BlogimageModel
    extra = 3

class BlogimageAdmin(admin.ModelAdmin):
    inlines = [BioInline,]

admin.site.register(BlogModel ,BlogimageAdmin)