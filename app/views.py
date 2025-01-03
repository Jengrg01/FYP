from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Makeup #for entry to database
from . forms import *
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
# write functions for database, based on function or class based views(api creations get easier), we apure working on mvt pattern

def home(request):
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

def artistlist(request):
     makeup = Makeup.objects.all()#no limitations
    #the context is in dictionary form
     context ={
        "artist": makeup
    }
     return render(request, "artists/artistlist.html",context)
# adding a form 
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
            
            messages.add_message(request, messages.SUCCESS, "Artist has been added successfully !")
            # to send back to another list when form is saved.
            return redirect('artistlist')
        else:
            messages.add_message(request, messages.ERROR, "Please verify all the fields !")
            return render(request,"artists/addartist.html", {"form": form} )
    return render(request,"artists/addartist.html",{"form": ArtistForm} )

def updateArtist(request, artist_id):
    instance = Makeup.objects.get(id=artist_id)
    if request.method == "POST":
        form = ArtistForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,"Artist data is updated successfully !")
            return redirect('artistlist')# return redirect('updateArtist', artist_id=artist_id) to pass artist_id through url 
        else:
            messages.add_message(request, messages.ERROR, "Error ! Data could not be updated !")
            return render(request, 'artists/updateartist.html',{"form": form})
    # to pass both form and product id in order to update a specific artist.
    context = {
        "form": ArtistForm(instance=instance)
    }
    return render(request, 'artists/updateartist.html', context)
def deleteArtist(request, artist_id):
    artist = Makeup.objects.get(id = artist_id)
    artist.delete()
    messages.add_message(request, messages.SUCCESS, "Artist has been deleted successfully !")
    return redirect('artistlist')

def categorylist(request):
    category = Category.objects.all()
    return render(request, 'artists/categorylist.html',{'category': category})

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

def deletecategory(request, category_id):
    category = Category.objects.get(id = category_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS, "Category has been deleted successfully !")
    return redirect('categorylist')

def specialitylist(request):
    speciality = Speciality.objects.all()
    return render(request, 'artists/specialitylist.html',{'speciality': speciality})

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

def deletespeciality(request, speciality_id):
    category = Speciality.objects.get(id = speciality_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS, "Speciality has been deleted successfully !")
    return redirect('specialitylist')

