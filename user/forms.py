from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from . models import *

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']
    
class LoginForm(AuthenticationForm):
    def __init__(self, request=None,*args, **kwargs):
        print(request)
        super().__init__(request=request,*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})

def ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = []