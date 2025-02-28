from django.urls import path
from .views import upload_image

urlpatterns = [
    path('predictmakeup/', upload_image, name='predict_makeup'),
]
