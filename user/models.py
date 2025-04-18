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
 

class ChatRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rooms')
    artist = models.ForeignKey(Makeup, on_delete=models.CASCADE, related_name='artist_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.user.username} and {self.artist.user.username}"
    

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"