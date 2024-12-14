from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# write functions for database, based on function or class based views(api creations get easier), we apure working on mvt pattern

def home(self):
    return HttpResponse("Welcome to Home Page")

def artist(self):
    return HttpResponse("Welcome to Artist Page")