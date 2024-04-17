from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm

class RegistrationForm(forms.Form):
    #Giving a specific html class to all fields
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'fields'
            
    fullname = forms.CharField(label= False, max_length=225, widget= forms.TextInput(attrs={'placeholder' : 'Full name', }))
    username = forms.CharField(label= False, max_length=30, widget=forms.TextInput(attrs={'placeholder' : 'Username'}))
    email = forms.EmailField(label= False, max_length=225, widget=forms.EmailInput(attrs={'placeholder' : 'Email'}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}))
    password1 = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder' : 'Confirm password'}))
    

    #This method prevent the registration of an account whit rapetitive Email.
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email address taken already!')
        return email
    
    #This method prevent the registration of an account whit rapetitive Usename.
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('This username taken already!')
        return username.lower()
    


    #split fullname field
    def clean_fullname(self):
        fullname = self.cleaned_data['fullname']
        if fullname:
            name_part = fullname.split()
            if len(name_part) >= 2:
                self.cleaned_data['firstname'] = name_part[0]
                self.cleaned_data['lastname'] = ' '.join(name_part[1:])
            else:
                self.cleaned_data['firstname'] = name_part[0]
                self.cleaned_data['lastname'] = ''    
        else:
            raise ValidationError("It seems like you didn't insert your Fullname!")
    
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError('Your password must be more than 8 characters!')
        digit_num = sum(1 for char in password if char.isdigit())
        if digit_num < 4:
            raise ValidationError('Your password must contain at least 4 digits!')
        return password
            

    def clean(self):
        cleaned_data = super().clean()
        pswrd = cleaned_data.get('password')
        pswrd1 = cleaned_data.get('password1')

        if pswrd and pswrd1 and pswrd != pswrd1:
            raise ValidationError('Passwords do not match!') 
        

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'fields'


    username = forms.CharField(max_length=225, label=False ,widget=forms.TextInput(attrs={'placeholder' : 'Username'}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        usernamelower = username.lower()
        return usernamelower

# customize email password reset form 
class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label=False, widget=forms.EmailInput(attrs={
        'placeholder' : 'Email',
        'class' : 'fields'
        }))
    