# to create forms according to model
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from . models import *

class ArtistForm(ModelForm):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(max_length=200)
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

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = ArtistPortfolio
        fields = ['gallery', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Add a caption (optional)'}),
        }