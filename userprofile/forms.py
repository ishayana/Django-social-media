from django import forms
from .models import PostModel, CommentModel

class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ('description','image',)
        labels = {
            'description' : False,
            'image' : False,
            'author' : False
        }

        widgets = {
            'description' : forms.Textarea(attrs={'placeholder' : "What's happening?",'col' : 1}),
        }


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ('description', 'image',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ('description',)
        labels = {
            'description' : False
        }

        widgets = {
            'description' : forms.Textarea(attrs=({"placeholder" : "Post your comment"}))
        }