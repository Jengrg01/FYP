# to create forms according to model
from django.forms import ModelForm
from . models import *

class ArtistForm(ModelForm):
    class Meta:
        model = Makeup
        fields = "__all__" #all fields should be shown

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class SpecialityForm(ModelForm):
    class Meta:
        model = Speciality
        fields = "__all__"