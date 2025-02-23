from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import *
from .auth import admin_only
from app.models import *
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

def loginUser(request):
    if request.method == "POST":
        print(request.POST)
        form = LoginForm(request=request,data=request.POST)
        print(form.data)
        if not form.is_valid():
            print("Form errors:", form.errors)
        if form.is_valid():
            # to read the data
            data = form.cleaned_data
            print("cleaned data:", data)
            user = authenticate(request, username = data['username'], password = data['password'])
            print(user)
            if user is not None:
                login(request, user)
                 # If user is superuser (admin)
                if user.is_superuser:
                    messages.add_message(request, messages.SUCCESS, "Successfully logged in as admin!")
                    return redirect('leader')  # Redirect to admin dashboard
                # User is authenticated, check for profile and user type
                try:
                    # Check if the user has a profile and if they are an artist
                    user_profile = UserProfile.objects.get(user=user)
                    print(user_profile.is_artist)
                    if user_profile.is_artist:
                        messages.add_message(request, messages.SUCCESS, "Successfully logged in as artist!")
                        return redirect('artist')  # Redirect to artist dashboard
                    else:
                        # If the user doesn't have a profile, proceed as a regular user
                        messages.add_message(request, messages.SUCCESS, "Successfully logged in!")
                        return redirect('home')  # Redirect to regular user dashboard
                except UserProfile.DoesNotExist as e:
                    # Handle the case where the user profile does not exist
                    print(e)
                    messages.add_message(request, messages.WARNING, "User profile not found.")
                    return redirect('login')
                
               
            else:
                messages.add_message(request, messages.ERROR, "Please verify all the fields.")
                return render (request, 'user/login.html',{"form": form})
    return render(request, 'user/login.html', {"form": LoginForm(request=request)})

def logout_user(request):
    logout(request)
    return redirect('login')

@admin_only
def Userlist(request):
    # Get all UserProfile objects where is_artist is False
    non_artist_users = UserProfile.objects.filter(is_artist=False)
    # To get the corresponding user objects
    non_artist_user_list = [user_profile.user for user_profile in non_artist_users]
    context = {'user_list': non_artist_user_list}
    return render(request, "artists/userlist.html", context)
@admin_only
def deleteUser(request, user_id):
    # Get the UserProfile object with the given ID or return a 404 error
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    user_profile.user.delete()
    messages.add_message(request, messages.SUCCESS, "User has been deleted successfully!")
    return redirect('userlist')


def artist_detail(request, artist_id):
    artist = Makeup.objects.get(id=artist_id)
    context = {
        'artist':artist
    }
    return render(request,"user/artistdetail.html",context)
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile

def user_detail(request, user_id):
    # Fetch UserProfile using user_id from the User model
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)  # Fetch profile linked to user
    context = {'current_user': user_profile}  # Pass user_profile, not just user
    return render(request, "user/userdetail.html", context)

def user_acc_settings(request):
    user = request.user
    form = ProfileForm(instance=user.userprofile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user.userprofile)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request,"user/accountsettings.html",context)