from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Makeup #for entry to database
from . forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from user.models import UserProfile  
from user.auth import admin_only
# Create your views here.
# write functions for database, based on function or class based views(api creations get easier), we apure working on mvt pattern

def home(request):
    user = request.user
    makeup = Makeup.objects.all().order_by('-id')[:4]#creating of 4 artists to be displayed in the card, shows the latest added artist at first
    #the context is in dictionary form
    context ={
        "makeup": makeup
    }
    return render(request, "artists/index.html",context)


def artist(request):
    makeup = Makeup.objects.all()#no limitations
    #the context is in dictionary form
    context ={
        "artist": makeup
    }
    return render(request, "artists/artistpage.html",context)

@admin_only
def artistlist(request):
     makeup = Makeup.objects.all()#no limitations
    #the context is in dictionary form
     context ={
        "artist": makeup
    }
     return render(request, "artists/artistlist.html",context)
# adding a form 
@admin_only
def addArtist(request):
    if request.method == "POST":
        # to send the data sent from method post, we need .FILES as we have images to send too
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
             # Create a User object for the artist
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            
            # Create a Makeup (Artist) object and associate it with the user
            artist = form.save(commit=False)
            artist.user = user
            artist.save()

            user_profile = UserProfile.objects.create(user=user, is_artist=True)
            
            messages.add_message(request, messages.SUCCESS, "Artist has been added successfully !")
            # to send back to another list when form is saved.
            return redirect('artistlist')
        else:
            messages.add_message(request, messages.ERROR, "Please verify all the fields !")
            return render(request,"artists/addartist.html", {"form": form} )
    return render(request,"artists/addartist.html",{"form": ArtistForm} )

@admin_only
def updateArtist(request, artist_id):
    # Retrieve the artist's Makeup object and associated User object
    artist = Makeup.objects.get(id=artist_id)
    user = artist.user  # This is the associated User object for this artist

    if request.method == "POST":
        form = ArtistForm(request.POST, request.FILES, instance=artist)

        if form.is_valid():
            # Get the cleaned data from the form
            cleaned_data = form.cleaned_data

            # If username or password is being changed, update the User object
            new_username = cleaned_data.get('username')
            new_password = cleaned_data.get('password')

            # Update User object (username and password)
            if new_username != user.username:
                user.username = new_username

            if new_password:  # Only update password if it's provided
                user.set_password(new_password)  # Don't store plain password
                user.save()  # Save the updated user object

            # Save the updated Makeup (artist) object
            form.save()

            # Optional: Update UserProfile if necessary (e.g., is_artist)
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.is_artist = True  # Ensure the user is marked as an artist
            user_profile.save()

            messages.add_message(request, messages.SUCCESS, "Artist data is updated successfully!")
            return redirect('artistlist')  # Redirect to the artist list after update
        else:
            messages.add_message(request, messages.ERROR, "Error! Data could not be updated!")
            return render(request, 'artists/updateartist.html', {"form": form})

    # If not a POST request, display the form with the existing data
    context = {
        "form": ArtistForm(instance=artist)
    }
    return render(request, 'artists/updateartist.html', context)
@admin_only
def deleteArtist(request, artist_id):
    artist = Makeup.objects.get(id = artist_id)
    artist.delete()
    messages.add_message(request, messages.SUCCESS, "Artist has been deleted successfully !")
    return redirect('artistlist')
@admin_only
def categorylist(request):
    category = Category.objects.all()
    return render(request, 'artists/categorylist.html',{'category': category})
@admin_only
def addcategory(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Category has been added successfully !")
            # to send back to another list when form is saved.
            return redirect('categorylist')
        else:
            messages.add_message(request, messages.ERROR, "Please verify field correctly !")
            return render(request,"artists/addcategory.html", {"form": form} )
    return render(request,"artists/addcategory.html",{"form": CategoryForm} )
@admin_only
def updatecategory(request,category_id):
    instance = Category.objects.get(id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,"Category is updated successfully !")
            return redirect('categorylist')
        else:
            messages.add_message(request, messages.ERROR, "Error ! Data could not be updated !")
            return render(request, 'artists/updatecategory.html',{"form": form})
    # to pass both form and product id in order to update a specific artist.
    context = {
        "form": CategoryForm(instance=instance)
    }
    return render(request, 'artists/updatecategory.html', context)
@admin_only
def deletecategory(request, category_id):
    category = Category.objects.get(id = category_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS, "Category has been deleted successfully !")
    return redirect('categorylist')
@admin_only
def specialitylist(request):
    speciality = Speciality.objects.all()
    return render(request, 'artists/specialitylist.html',{'speciality': speciality})
@admin_only
def addspeciality(request):
    if request.method == "POST":
        form = SpecialityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Speciality has been added successfully !")
            return redirect('specialitylist')
        else:
            messages.add_message(request, messages.ERROR, "Please verify field correctly !")
            return render(request,"artists/addspeciality.html", {"form": form} )
    return render(request,"artists/addspeciality.html",{"form": SpecialityForm} )
@admin_only
def updatespeciality(request,speciality_id):
    instance = Speciality.objects.get(id=speciality_id)
    if request.method == "POST":
        form = SpecialityForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,"Speciality is updated successfully !")
            return redirect('specialitylist')
        else:
            messages.add_message(request, messages.ERROR, "Error ! Data could not be updated !")
            return render(request, 'artists/updatespeciality.html',{"form": form})
    # to pass both form and product id in order to update a specific artist.
    context = {
        "form": SpecialityForm(instance=instance)
    }
    return render(request, 'artists/updatespeciality.html', context)
@admin_only
def deletespeciality(request, speciality_id):
    category = Speciality.objects.get(id = speciality_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS, "Speciality has been deleted successfully !")
    return redirect('specialitylist')

