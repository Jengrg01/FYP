from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import * #for entry to database
from . forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from user.models import UserProfile  
from user.auth import admin_only
from .utils import *
# Create your views here.
# write functions for database, based on function or class based views(api creations get easier), we apure working on mvt pattern

def policy(request):
    return render(request,"artists/policy.html")

def terms(request):
    return render(request,"artists/terms.html")

def aboutus(request):
    return render(request,"artists/aboutus.html")

def services(request):
    return render(request,"artists/services.html")

def contactpage(request):
    return render(request,"artists/contact.html")

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
    
    categories = Category.objects.all()
    specialities = Speciality.objects.all()

       # Get query parameters for sorting and filtering
    sort_by = request.GET.get('sort_by', None)  # Sorting (default: None) 
    category_filter = request.GET.get('category', None)
    speciality_filter = request.GET.get('speciality', None)

    # Apply category filter
    if category_filter:
        makeup = makeup.filter(category__category_name=category_filter)
    
    # Apply speciality filter
    if speciality_filter:
        makeup = makeup.filter(speciality__speciality_name=speciality_filter)

    # Apply sorting if a valid sorting parameter is provided
    if sort_by:
        makeup = makeup.order_by(sort_by)

    # Pass everything to the template
    context = {
        "artist": makeup,
        "sort_by": sort_by,
        'categories': categories,
        'specialities': specialities,
        'category_filter': category_filter,
        'speciality_filter': speciality_filter,
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
            email = form.cleaned_data['email']

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email  # This is the primary email storage
            )
            
            
            # Create a Makeup (Artist) object and associate it with the user
            artist = form.save(commit=False)
            artist.user = user
            artist.save()

            UserProfile.objects.create(user=user, is_artist=True)
            
            messages.add_message(request, messages.SUCCESS, "Artist has been added successfully !")
            # to send back to another list when form is saved.
            send_email_to_artist(username, password, email)
            return redirect('artistlist')
        else:
            messages.add_message(request, messages.ERROR, "Please verify all the fields !")
            return render(request,"artists/addartist.html", {"form": form} )
    return render(request,"artists/addartist.html",{"form": ArtistForm} )

@admin_only
def updateArtist(request, artist_id):
    artist = Makeup.objects.get(id=artist_id)
    user = artist.user

    if request.method == "POST":
        form = ArtistForm(request.POST, request.FILES, instance=artist)

        if form.is_valid():
            # Get cleaned data
            cleaned_data = form.cleaned_data
            
            # Update User fields
            user.username = cleaned_data.get('username', user.username)
            user.email = cleaned_data.get('email', user.email)  # Always update User.email
            
            if cleaned_data.get('password'):  # Only update if password changed
                user.set_password(cleaned_data['password'])
            
            user.save()  # Save user changes first

            # Save artist profile
            artist = form.save(commit=False)
            artist.user = user  # Ensure relationship is maintained
            artist.save()

            # Update UserProfile (only is_artist flag, no email)
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.is_artist = True
            user_profile.save()

            messages.success(request, "Artist updated successfully!")
            send_email_to_artist_update(user.username, cleaned_data.get('password'), user.email)
            return redirect('artistlist')
        else:
            messages.error(request, "Please correct the errors below!")
    else:
        form = ArtistForm(instance=artist)

    return render(request, 'artists/updateartist.html', {"form": form})
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

