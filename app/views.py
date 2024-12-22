from django.shortcuts import render
from django.http import HttpResponse
from . models import Makeup #for entry to database
# Create your views here.
# write functions for database, based on function or class based views(api creations get easier), we apure working on mvt pattern

def home(request):
    makeup = Makeup.objects.all()
    #the context is in dictionary form
    context ={
        "makeup": makeup
    }
    return render(request, "artists/index.html",context)


def artist(request):
    return render(request, "artists/artistpage.html")