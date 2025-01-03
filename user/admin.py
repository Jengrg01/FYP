from django.contrib import admin
from .models import UserProfile  # Import your model

# Register your model with the admin interface
admin.site.register(UserProfile)

