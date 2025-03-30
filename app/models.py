from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# create models through object relation mapping
class Speciality(models.Model):
    speciality_name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.speciality_name
    
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.category_name

class Makeup(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    artist_name = models.CharField(max_length=100)
    rate = models.IntegerField()
    artist_description = models.CharField(max_length=5000, blank=True, null=True)
    speciality = models.ForeignKey(Speciality, on_delete = models.CASCADE, null = True)
    image = models.ImageField(upload_to='static/uploads',null=True,default = "profilepic.png" ,blank=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, null = True)
    cover_pic = models.ImageField(
        upload_to='static/uploads/',
        default="default-cover.jpg", null=True,blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, blank= True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank= True, null = True)
    def __str__(self):
        return self.artist_name
    
class ArtistPortfolio(models.Model):
    artist = models.ForeignKey(Makeup, on_delete=models.CASCADE, related_name='portfolio')
    gallery = models.ImageField(upload_to='static/portfolio/') 
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Portfolio item for {self.artist.artist_name}"