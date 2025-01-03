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