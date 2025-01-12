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
    artist_description = models.CharField(max_length=300)
    speciality = models.ForeignKey(Speciality, on_delete = models.CASCADE, null = True)
    image = models.FileField(upload_to='static/uploads',null=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, null = True)
    def __str__(self):
        return self.artist_name
    

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
