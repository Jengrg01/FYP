# to create forms according to model
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from . models import *
import datetime
from datetime import datetime, timedelta, time, date

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

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = ArtistPortfolio
        fields = ['image', 'caption']


TIME_CHOICES = [
    ('09:00', '09:00 AM - 11:00 AM'),
    ('11:30', '11:30 AM - 1:30 PM'),
    ('14:00', '2:00 PM - 4:00 PM'),
    ('17:00', '5:00 PM - 7:00 PM'),
    ('full_day', 'Full Day (09:00 AM - 7:00 PM)'),
]

class TimeSlotForm(forms.ModelForm):
    time_slot = forms.ChoiceField(choices=TIME_CHOICES, label="Available Time Slots")
    
    class Meta:
        model = TimeSlot
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'min': datetime.today().strftime('%Y-%m-%d')
            }),
        }