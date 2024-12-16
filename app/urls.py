# must make urls in app by yourself, it is not a given file by django in app
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("artist/", views.artist),
]
