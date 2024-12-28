from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Makeup #for entry to database
from . forms import *
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
            form.save()
            # to send back to another list when form is saved.
            return redirect('/artists/artistlist')
        else:
            return render(request,"artists/addartist.html", {"form": form} )
    return render(request,"artists/addartist.html",{"form": ArtistForm} )