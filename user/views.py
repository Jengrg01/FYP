from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import *
# Create your views here.

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.add_message(request, messages.SUCCESS, "User has been registered successfully")
            return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, "Please verify all the fields")
            return render(request, 'user/register.html', {"form": form})
    context = {
        'form': UserRegistrationForm
    }
    return render(request, 'user/register.html', context)

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # to read the data
            data = form.cleaned_data
            user = authenticate(request, username = data['username'], password = data['password'])
            if user is not None:
                login(request, user)
                # User is authenticated, check for profile and user type
                try:
                    # Check if the user has a profile and if they are an artist
                    user_profile = UserProfile.objects.get(user=user)
                    if user_profile.is_artist:
                        messages.add_message(request, messages.SUCCESS, "Successfully logged in as artist!")
                        return redirect('artist')  # Redirect to artist dashboard
                except UserProfile.DoesNotExist:
                    # If the user doesn't have a profile, proceed as a regular user
                    messages.add_message(request, messages.SUCCESS, "Successfully logged in!")
                    return redirect('home')  # Redirect to regular user dashboard
                
                # If user is superuser (admin)
                if user.is_superuser:
                    messages.add_message(request, messages.SUCCESS, "Successfully logged in as admin!")
                    return redirect('adminpage')  # Redirect to admin dashboard
            else:
                messages.add_message(request, messages.ERROR, "Please verify all the fields.")
                return render (request, 'user/login.html',{"form": form})
    return render(request, 'user/login.html', {"form": LoginForm()})