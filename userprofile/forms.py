from django import forms
from .models import PostModel, CommentModel
from accounts.models import UserprofileModel

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


class SearchForm(forms.Form):
    search = forms.CharField(max_length=225, label=False, widget=forms.TextInput(attrs={'placeholder' : 'Search...'}))



class UserbioForm(forms.ModelForm):
    class Meta:
        model = UserprofileModel
        fields = ['bio', 'avatar']