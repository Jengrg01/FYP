from django.urls import path
from .  views import *
from user.views import admin_login
urlpatterns = [
   path("", leader, name = 'leader'),
   path("adminlogin/", admin_login, name='admin_login'),
]
