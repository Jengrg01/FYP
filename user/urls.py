from django.urls import path
from app import views
from . views import *
urlpatterns = [
    path("",views.home, name = 'home'),
    path("register/",register_user, name='register' ),
    path("login/",loginUser, name='login' ),
    path("userlist/", Userlist, name='userlist'),
    path('deleteUser/<int:user_id>/', deleteUser, name='deleteUser'),
]