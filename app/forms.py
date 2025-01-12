# to create forms according to model
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from . models import *

class ArtistForm(ModelForm):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    class Meta:
        model = Makeup
        exclude = ['user'] 

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class SpecialityForm(ModelForm):
    class Meta:
        model = Speciality
        fields = "__all__"


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message'}),
        }
