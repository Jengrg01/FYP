from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from . models import *
from app.models import *
from django.utils import timezone
from django.db.models import Q


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name', 'email','password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone_number"].widget.attrs["required"] = True
        
            
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        # this for email authentication, so that after the account is made the user will be set as inactive until the email is confirmed, this is for security reasons
        user.is_active = False
        if commit:
            user.save()
            UserProfile.objects.create(user=user, phone_number=self.cleaned_data["phone_number"])
        return user
    

class LoginForm(AuthenticationForm):
    def __init__(self, request=None,*args, **kwargs):
        print(request)
        super().__init__(request=request,*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user','is_artist']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']

class ArtistProfileForm(forms.ModelForm):
    class Meta:
        model = Makeup
        fields = ['artist_name', 'rate', 'artist_description', 'speciality', 'category', 'image', 'cover_pic']
        widgets = {
            'artist_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter artist name'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'artist_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your work...'}),
            'speciality': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'cover_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }


#For user to book an artist
class BookingForm(forms.Form):
    time_slot = forms.ModelChoiceField(queryset=None, label="Select Time Slot", empty_label=None)

    def __init__(self, artist=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if artist:
            current_time = timezone.now()

            # Filter out past and booked time slots
            available_slots = TimeSlot.objects.filter(
                artist=artist,
                is_booked=False
            ).filter(
                Q(date__gt=current_time.date()) |
                Q(date=current_time.date(), start_time__gt=current_time.time())
            ).order_by('date', 'start_time')

            self.fields['time_slot'].queryset = available_slots

            # Optional user-friendly empty label if no slots exist
            if not available_slots.exists():
                self.fields['time_slot'].empty_label = "No available time slots"


#for user to leave review
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} ⭐') for i in range(1, 6)]),
            'review_text': forms.Textarea(attrs={'placeholder': 'Write your review...'}),
        }