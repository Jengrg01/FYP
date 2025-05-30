# must make urls in app by yourself, it is not a given file by django in app
from django.urls import path
from . import views 
# from .views import *

urlpatterns = [
    path("artist/", views.artist, name='artist'),
    path("addartist/", views.addArtist, name='addArtist'),
    path("artistlist/", views.artistlist, name='artistlist'),
    path("updateartist/<int:artist_id>", views.updateArtist, name='updateArtist'),
    path("deleteartist/<int:artist_id>", views.deleteArtist, name='deleteArtist'),
    path("addcategory/", views.addcategory, name='addcategory'),
    path("categorylist/", views.categorylist, name='categorylist'),
    path("updatecategory/<int:category_id>", views.updatecategory, name='updatecategory'),
    path("deletecategory/<int:category_id>", views.deletecategory, name='deletecategory'),
    path("addspeciality/", views.addspeciality, name='addspeciality'),
    path("specialitylist/", views.specialitylist, name='specialitylist'),
    path("updatespeciality/<int:speciality_id>", views.updatespeciality, name='updatespeciality'),
    path("deletespeciality/<int:speciality_id>", views.deletespeciality, name='deletespeciality'),
    path("policy/", views.policy, name='policy'),
    path("contact/", views.contactpage, name='contact'),
    path("terms/", views.terms, name='terms'),
    path("aboutus/", views.aboutus, name='aboutus'),
    path("services/", views.services, name='services'),
    path("faq/", views.faq, name='faq'),
    path("timeslot/", views.add_availability, name='timeslot'),
    path('dashboard/', views.artist_dashboard, name='artistdashboard'),
    path('deleteslot/<int:slot_id>/', views.delete_time_slot, name='delete_slot'),
    path('notifications/', views.notifications_view, name='artist_notifications'),
    path('guidelines/', views.guidelines, name='guidelines'),
    path('community/', views.community, name='community'),
]
