from django.contrib import admin
from .models import PostModel, FollowModel, CommentModel , LikeModel

class PostModelAdmin(admin.ModelAdmin):
    list_display = ('author', 'description', 'created')
    ordering = ('created',)

admin.site.register(PostModel, PostModelAdmin)


class FollowModelAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created',)
    ordering = ('-created',)



admin.site.register(FollowModel, FollowModelAdmin)

    

@admin.register(CommentModel)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('reply', 'description', 'author', 'is_reply')

admin.site.register(LikeModel)