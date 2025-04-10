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
    artist = models.ForeignKey(Makeup, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='static/portfolio/') 
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Portfolio item for {self.artist.artist_name}"
    


#The timeslot model for the artist to add their availabilty time
class TimeSlot(models.Model):
    artist = models.ForeignKey(Makeup, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.artist.artist_name} - {self.date} ({self.start_time} to {self.end_time})"
    


#The model for user to book an artist through the time slot that is chosen by the artist
class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.ForeignKey(Makeup, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    def __str__(self):
        return f"{self.user.username} booked {self.artist.artist_name} on {self.time_slot.date} at {self.time_slot.start_time} ({self.status})"
    

#Model for the notification feature on artist side 
class Notification(models.Model):
    artist = models.ForeignKey(Makeup, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
