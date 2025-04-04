from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from .forms import *
from .models import *
from .auth import *
from app.models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile
# Create your views here.

def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("User Registered:", user.username, user.email)
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

@artist_required
def artist_profile(request, artist_id):
    artist = Makeup.objects.get(id=artist_id)
    context = {
        'artist':artist
    }
    return render(request,"user/artistprofile.html",context)

@artist_required
def artist_acc_settings(request):
    artist = Makeup.objects.get(user=request.user)
    if request.method == "POST":
        form = ArtistProfileForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("artistprofile", artist_id=artist.id)
    else:
        form = ArtistProfileForm(instance=artist)
    context = {
        'form': form
    }
    return render(request, "user/artistsettings.html",context)

@user_required
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user) 
    context = {
        'user':user,
        'current_user': user_profile
        }  
    return render(request, "user/userdetail.html", context)

@user_required
def user_acc_settings(request):
    user = request.user
    profile = user.userprofile 
    user_form = UserUpdateForm(instance=user)
    profile_form = ProfileForm(instance=profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect(reverse("userprofile", kwargs={"user_id": user.id})) 

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, "user/accountsettings.html", context)
