from django.db import models

# Create your models here.
# create models through object relation mapping
class Speciality(models.Model):
    speciality_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.speciality_name
    
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category_name

class Makeup(models.Model):
    artist_name = models.CharField(max_length=100)
    rate = models.IntegerField()
    artist_description = models.CharField(max_length=100)
    speciality = models.ForeignKey(Speciality, on_delete = models.CASCADE, null = True)
    image = models.URLField(null=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, null = True)
    def __str__(self):
        return self.artist_name
    
