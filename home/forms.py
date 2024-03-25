from django import forms

class tesd(forms.Form):
    username = forms.CharField(max_length=225, label=False ,widget=forms.TextInput(attrs={'placeholder' : 'Username'}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}))