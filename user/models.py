from django.db import models
from django.contrib.auth.models import User
from app.models import *

class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null= True, default = "profilepic.png", blank=True)
    is_artist = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True) 
    def __str__(self):
        return self.user.username if self.user else "No User Assigned"
 


