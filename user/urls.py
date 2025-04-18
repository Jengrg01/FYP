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
    path('upload-image/', upload_gallery_image, name='upload_gallery_image'),
    path('booking/<int:artist_id>/', book_time_slot, name='booking'),
    path('bookhistory/', booking_history, name='bookhistory'),
    path('cancelbooking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('completebooking/<int:booking_id>/', complete_booking, name='complete_booking'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
    path('review/<int:artist_id>/', submit_review, name='submit_review'),
    path('userchat/', user_chat_list, name='user_chat_list'),  # User chat list
    path('artistchat/', artist_chat_list, name='artist_chat_list'),  # Artist chat list
    path('chat/user/<int:room_id>/', chat_room_user, name='chat_room_user'),
    path('chat/artist/<int:room_id>/', chat_room_artist, name='chat_room_artist'),
]