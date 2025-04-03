from django.urls import path
from app import views
from . views import *
urlpatterns = [
    path("",views.home, name = 'home'),
    path("register/",register_user, name='register' ),
    path("login/",loginUser, name='login' ),
    path("logout/",logout_user, name='logout' ),
    path("userlist/", Userlist, name='userlist'),
    path('deleteUser/<int:user_id>/', deleteUser, name='deleteUser'),
    path("artistdetail/<int:artist_id>/", artist_detail, name='artistDetail'),
    path("userdetail/<int:user_id>/", user_detail, name='userprofile'),
    path("usersettings/", user_acc_settings, name='usersettings'),
    path("artistprofile/<int:artist_id>/", artist_profile, name='artistprofile'),
    path("artistsettings/", artist_acc_settings, name='artistsettings'),
    
]