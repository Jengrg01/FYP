# must make urls in app by yourself, it is not a given file by django in app
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("artist/", views.artist, name='artist'),
    path("addartist/", views.addArtist, name='addArtist'),
    path("artists/artistlist/", views.artistlist, name='artistlist'),
]
