# to create forms according to model
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from . models import *
import datetime
from datetime import datetime, timedelta, time

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



class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['date', 'start_time']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'min': datetime.today().strftime('%Y-%m-%d')
            }),
            'start_time': forms.Select(choices=[
                ('09:00', '09:00 AM - 11:00 AM'),
                ('11:30', '11:30 AM - 1:30 PM'),
                ('14:00', '2:00 PM - 4:00 PM'),
                ('17:00', '5:00 PM - 7:00 PM'),
            ]),
        }

    def __init__(self, *args, **kwargs):
        self.artist = kwargs.pop('artist', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        start_time_str = cleaned_data.get("start_time")

        if not date or not start_time_str:
            return cleaned_data

        # Convert start_time_str (which is already a string) into a time object
        start_time = start_time_str if isinstance(start_time_str, time) else datetime.strptime(str(start_time_str), "%H:%M").time()
        end_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=2)).time()

        cleaned_data["start_time"] = start_time
        cleaned_data["end_time"] = end_time

        # Prevent past date or current day with past time
        now = datetime.now()
        if date < now.date() or (date == now.date() and start_time <= now.time()):
            raise forms.ValidationError("Cannot add past time slots.")

        # Prevent duplicate slot
        if TimeSlot.objects.filter(
            artist=self.artist,
            date=date,
            start_time=start_time
        ).exists():
            raise forms.ValidationError("This time slot is already added.")

        return cleaned_data