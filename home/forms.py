from django import forms

from .models import BlogModel, BlogimageModel
from django.forms import inlineformset_factory

class BlogsearchForm(forms.Form):
    search = forms.CharField(max_length=225, label=False, widget=forms.TextInput(attrs={'placeholder' : 'Search...'}))