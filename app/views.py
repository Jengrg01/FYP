from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from . models import * 
from . forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from user.models import *
from django.http import JsonResponse 
from user.auth import *
from .utils import *
from datetime import datetime, timedelta, time
from django.utils import timezone
from django.utils.timezone import make_aware, is_naive, now

# Create your views here.
# write functions for database, based on function or class based views(api creations get easier), we apure working on mvt pattern
def guidelines(request):
    return render(request,"artists/guidelines.html")

def faq(request):
    return render(request,"artists/faq.html")

def policy(request):
    return render(request,"artists/policy.html")

def terms(request):
    return render(request,"artists/terms.html")

def aboutus(request):
    return render(request,"artists/aboutus.html")

def services(request):
    return render(request,"artists/services.html")

@user_required
def contactpage(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user) 
    # Pass the user's data to the template
    context = {
        'user':user,
        'current_user': user_profile,
    }
    return render(request,"artists/contact.html",context)

def home(request):
    user = request.user
    makeup = Makeup.objects.all().order_by('-id')[:4]#creating of 4 artists to be displayed in the card, shows the latest added artist at first
    #the context is in dictionary form
    context ={
        "makeup": makeup
    }
    return render(request, "artists/index.html",context)


def artist(request):
    makeup = Makeup.objects.all()#no limitations
    
    categories = Category.objects.all()
    specialities = Speciality.objects.all()

       # Get query parameters for sorting and filtering
    sort_by = request.GET.get('sort_by', None)  # Sorting (default: None) 
    category_filter = request.GET.get('category', None)
    speciality_filter = request.GET.get('speciality', None)

    # Apply category filter
    if category_filter:
        makeup = makeup.filter(category__category_name=category_filter)
    
    # Apply speciality filter
    if speciality_filter:
        makeup = makeup.filter(speciality__speciality_name=speciality_filter)

    # Apply sorting if a valid sorting parameter is provided
    if sort_by:
        makeup = makeup.order_by(sort_by)

    # Pass everything to the template
    context = {
        "artist": makeup,
        "sort_by": sort_by,
        'categories': categories,
        'specialities': specialities,
        'category_filter': category_filter,
        'speciality_filter': speciality_filter,
    }
    return render(request, "artists/artistpage.html",context)

@admin_only
def artistlist(request):
     makeup = Makeup.objects.all()#no limitations
    #the context is in dictionary form
     context ={
        "artist": makeup
    }
     return render(request, "artists/artistlist.html",context)
# adding a form 
@admin_only
def addArtist(request):
    if request.method == "POST":
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if the username already exists
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken, please try again with a different one.")
                return render(request, "artists/addartist.html", {"form": form})

            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email  
            )

            artist = form.save(commit=False)
            artist.user = user
            artist.save()

            UserProfile.objects.create(user=user, is_artist=True)
            
            messages.add_message(request, messages.SUCCESS, "Artist has been added successfully!")
            send_email_to_artist(username, password, email)
            return redirect('artistlist')
        else:
            messages.add_message(request, messages.ERROR, "Please verify all the fields!")
            return render(request, "artists/addartist.html", {"form": form})
    return render(request, "artists/addartist.html", {"form": ArtistForm})

@admin_only
def updateArtist(request, artist_id):
    artist = Makeup.objects.get(id=artist_id)
    user = artist.user

    if request.method == "POST":
        form = ArtistForm(request.POST, request.FILES, instance=artist)

        if form.is_valid():
            # Check if the username already exists and is different from the current user's username
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username', user.username)

            if username != user.username and User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken, please try again with a different one.")
                return render(request, 'artists/updateartist.html', {"form": form})

            # Update User fields
            user.username = username
            user.email = cleaned_data.get('email', user.email)  # Always update User.email
            
            if cleaned_data.get('password'):  # Only update if password changed
                user.set_password(cleaned_data['password'])

            user.save()  # Save user changes first

            # Save artist profile
            artist = form.save(commit=False)
            artist.user = user  # Ensure relationship is maintained
            artist.save()

            # Update UserProfile (only is_artist flag, no email)
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.is_artist = True
            user_profile.save()

            messages.success(request, "Artist updated successfully!")
            send_email_to_artist_update(user.username, cleaned_data.get('password'), user.email)
            return redirect('artistlist')
        else:
            messages.error(request, "Please correct the errors below!")
    else:
        form = ArtistForm(instance=artist)

    return render(request, 'artists/updateartist.html', {"form": form})


@admin_only
def deleteArtist(request, artist_id):
    artist = Makeup.objects.get(id = artist_id)
    artist.delete()
    messages.add_message(request, messages.SUCCESS, "Artist has been deleted successfully !")
    return redirect('artistlist')
@admin_only
def categorylist(request):
    category = Category.objects.all()
    return render(request, 'artists/categorylist.html',{'category': category})
@admin_only
def addcategory(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Category has been added successfully !")
            # to send back to another list when form is saved.
            return redirect('categorylist')
        else:
            messages.add_message(request, messages.ERROR, "Please verify field correctly !")
            return render(request,"artists/addcategory.html", {"form": form} )
    return render(request,"artists/addcategory.html",{"form": CategoryForm} )
@admin_only
def updatecategory(request,category_id):
    instance = Category.objects.get(id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,"Category is updated successfully !")
            return redirect('categorylist')
        else:
            messages.add_message(request, messages.ERROR, "Error ! Data could not be updated !")
            return render(request, 'artists/updatecategory.html',{"form": form})
    # to pass both form and product id in order to update a specific artist.
    context = {
        "form": CategoryForm(instance=instance)
    }
    return render(request, 'artists/updatecategory.html', context)
@admin_only
def deletecategory(request, category_id):
    category = Category.objects.get(id = category_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS, "Category has been deleted successfully !")
    return redirect('categorylist')
@admin_only
def specialitylist(request):
    speciality = Speciality.objects.all()
    return render(request, 'artists/specialitylist.html',{'speciality': speciality})
@admin_only
def addspeciality(request):
    if request.method == "POST":
        form = SpecialityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Speciality has been added successfully !")
            return redirect('specialitylist')
        else:
            messages.add_message(request, messages.ERROR, "Please verify field correctly !")
            return render(request,"artists/addspeciality.html", {"form": form} )
    return render(request,"artists/addspeciality.html",{"form": SpecialityForm} )
@admin_only
def updatespeciality(request,speciality_id):
    instance = Speciality.objects.get(id=speciality_id)
    if request.method == "POST":
        form = SpecialityForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,"Speciality is updated successfully !")
            return redirect('specialitylist')
        else:
            messages.add_message(request, messages.ERROR, "Error ! Data could not be updated !")
            return render(request, 'artists/updatespeciality.html',{"form": form})
    # to pass both form and product id in order to update a specific artist.
    context = {
        "form": SpecialityForm(instance=instance)
    }
    return render(request, 'artists/updatespeciality.html', context)
@admin_only
def deletespeciality(request, speciality_id):
    category = Speciality.objects.get(id = speciality_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS, "Speciality has been deleted successfully !")
    return redirect('specialitylist')

#This function is used to add the form from which artist can reserve the available timeslots they have for their clients

@artist_required
def add_availability(request):
    try:
        artist = Makeup.objects.get(user=request.user)
    except Makeup.DoesNotExist:
        return HttpResponse("You are not registered as an artist.")

    if request.method == "POST":
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time_slot = form.cleaned_data['time_slot']
            now = datetime.now()
            
            # To convert time slot to actual times
            if time_slot == 'full_day':
                start_time = time(9, 0)   # 9:00 AM
                end_time = time(19, 0)    # 7:00 PM
            else:
                start_time = datetime.strptime(time_slot, "%H:%M").time()
                end_time = (datetime.combine(date, start_time) + timedelta(hours=2)).time()
            
            #This is to check if time slot is in the past, so that the artist may not be able to book already past date and time
            if date < now.date() or (date == now.date() and end_time <= now.time()):
                messages.error(request, "You can't add time slots that have already passed.")
                return render(request, 'artists/timeslot.html', {'form': form})
            
            # Checking for duplicate slots in the database
            if TimeSlot.objects.filter(artist=artist, date=date, start_time=start_time).exists():
                messages.error(request, "This time slot is already added.")
                return render(request, 'artists/timeslot.html', {'form': form})
            
            # Creating the time slot which is stored in db
            TimeSlot.objects.create(
                artist=artist,
                date=date,
                start_time=start_time,
                end_time=end_time,
                is_booked=False
            )
            
            messages.success(request, "Time slot added successfully!")
            return redirect('timeslot')
    
    else:
        form = TimeSlotForm()
    
    return render(request, 'artists/timeslot.html', {'form': form})


@artist_required
def artist_dashboard(request):
    artist = get_object_or_404(Makeup, user=request.user)
    today = now().date()
    days = [today + timedelta(days=i) for i in range(3)]

    # Get all relevant slots
    time_slots = TimeSlot.objects.filter(artist=artist, date__in=days).order_by('date', 'start_time')

    # Get all relevant bookings
    bookings = Booking.objects.filter(time_slot__in=time_slots).select_related('time_slot', 'user')

    booking_map = {b.time_slot.id: b for b in bookings}
    current_time = now()

    # Prepare schedule data
    schedule = []
    for slot in time_slots:
        slot_start = datetime.combine(slot.date, slot.start_time)
        if is_naive(slot_start):
            slot_start = make_aware(slot_start)

        booking = booking_map.get(slot.id)
        can_delete = current_time < slot_start and (not booking or booking.status == 'cancelled')

        schedule.append({
            'slot_id': slot.id,
            'date': slot.date,
            'time': f"{slot.start_time} - {slot.end_time}",
            'user': booking.user.username if booking else None,
            'status': booking.status if booking else 'available',
            'is_booked': bool(booking),
            'can_delete': can_delete
        })

    return render(request, 'artists/dashboard.html', {'schedule': schedule, 'today': today})



@artist_required
def delete_time_slot(request, slot_id):
    slot = get_object_or_404(TimeSlot, id=slot_id, artist__user=request.user)

    slot_start = datetime.combine(slot.date, slot.start_time)
    if is_naive(slot_start):
        slot_start = make_aware(slot_start)

    # Check if the slot can be deleted (either it's available, or the booking is cancelled)
    if now() < slot_start and (not Booking.objects.filter(time_slot=slot).exists() or 
                               Booking.objects.filter(time_slot=slot, status='cancelled').exists()):
        slot.delete()
        messages.success(request, "Time slot deleted successfully.")
    else:
        messages.error(request, "Cannot delete a booked or past time slot.")

    return redirect('artistdashboard')


@artist_required
def notifications_view(request):
    artist = get_object_or_404(Makeup, user=request.user)
    notifications = Notification.objects.filter(artist=artist).order_by('-timestamp')

    # Optional: mark all unread notifications as read
    notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'artists/notifications.html', {'notifications': notifications})


