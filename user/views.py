from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from .forms import *
from .models import *
from .auth import *
from app.models import *
from app.forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile
from django.utils import timezone
from django.utils.timezone import make_aware, is_naive, now
from datetime import datetime
from app.utils import *
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
# Create your views here.
# for email authentication, urlsafe_base64_encode and decode are used which are utility functions that safely encode and decode data in my case was uid for activation links in url which is sent to the user's email, encode occurs in utils.py decode in activate account view



def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_activation_email(request, user)
            print("User Registered:", user.username, user.email)
            messages.add_message(request, messages.SUCCESS, "User has been registered successfully")
            return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, "Please verify all the fields")
            return render(request, 'user/register.html', {"form": form})
    context = {
        'form': UserRegistrationForm
    }
    return render(request, 'user/register.html', context)

#email authentication view after registration
def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated! You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid or expired.")
        return redirect('register')


def loginUser(request):
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            user_type = request.POST.get('user_type', 'user')  # Get the selected user type

            # First check: if the user selected 'artist' but the account is not an artist, block it.
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if not user.is_active:
                    messages.error(request, "Account inactive. Please check your email to activate your account.")
                    return redirect('login')
                login(request, user)

                try:
                    user_profile = UserProfile.objects.get(user=user)

                    # If they selected 'Artist' but the user is not an artist, show this alert box
                    if user_type == 'artist' and not user_profile.is_artist:
                        messages.error(request, "This account is not an artist. Please try again.")
                        return redirect('login')
                    
                    if user_type == 'user' and user_profile.is_artist:
                        messages.error(request, "This account is not a user. Please try again.")
                        return redirect('login')

                    # If the account matches the selected user type, proceed with the appropriate action
                    if user_profile.is_artist:
                        try:
                            artist = Makeup.objects.get(user=user)
                            messages.success(request, "Successfully logged in as artist!")
                            return redirect('artistdashboard')
                        except Makeup.DoesNotExist:
                            messages.error(request, "Artist profile not found.")
                            return redirect('login')
                    else:
                        messages.success(request, "Successfully logged in!")
                        return redirect('home')

                except UserProfile.DoesNotExist:
                    messages.warning(request, "User profile not found.")
                    return redirect('login')
            else:
                messages.error(request, "Invalid username or password.")

    else:
        form = LoginForm(request=request)

    return render(request, 'user/login.html', {"form": form})


def admin_login(request):
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('login')  
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                messages.success(request, "Successfully logged in as admin!")
                return redirect('leader')  
            else:
                messages.error(request, "Invalid credentials or you are not an admin.")
    else:
        form = AuthenticationForm()

    return render(request, 'leaderpage/adminlogin.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')

@admin_only
def Userlist(request):
    # Get all UserProfile objects where is_artist is False
    non_artist_users = UserProfile.objects.filter(is_artist=False)
    # To get the corresponding user objects
    non_artist_user_list = [user_profile.user for user_profile in non_artist_users]
    context = {'user_list': non_artist_user_list}
    return render(request, "artists/userlist.html", context)
@admin_only
def deleteUser(request, user_id):
    # Get the UserProfile object with the given ID or return a 404 error
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    user_profile.user.delete()
    messages.add_message(request, messages.SUCCESS, "User has been deleted successfully!")
    return redirect('userlist')


def artist_detail(request, artist_id):
    artist = get_object_or_404(Makeup, id=artist_id)
    gallery_images = artist.gallery_images.all()
    reviews = artist.reviews.select_related('user').all().order_by('-created_at')  
    
    existing_review = None
    if request.user.is_authenticated:
        existing_review = Review.objects.filter(user=request.user, artist=artist).first()

    form = ReviewForm(instance=existing_review) if request.user.is_authenticated else None
    
    context = {
        'artist': artist,
        'gallery_images': gallery_images,
        'reviews': reviews,
        'form': form,
        'existing_review': existing_review,
    }
    return render(request, "user/artistdetail.html", context)


@artist_required
def artist_profile(request, artist_id):
    artist = Makeup.objects.get(id=artist_id)
    gallery_images = artist.gallery_images.all()
    reviews = artist.reviews.select_related('user').all()
    context = {
        'artist':artist,
        'gallery_images': gallery_images,
        'reviews' : reviews
    }
    return render(request,"user/artistprofile.html",context)


@artist_required
def artist_acc_settings(request):
    artist = Makeup.objects.get(user=request.user)
    if request.method == "POST":
        form = ArtistProfileForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS, "Your profile has been updated successfully!")
            return redirect("artistprofile", artist_id=artist.id)
    else:
        form = ArtistProfileForm(instance=artist)
    context = {
        'form': form
    }
    return render(request, "user/artistsettings.html",context)

@artist_required
def upload_gallery_image(request):
    artist = Makeup.objects.get(user=request.user)

    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            gallery_image = form.save(commit=False)
            gallery_image.artist = artist
            gallery_image.save()
            return redirect('artistprofile', artist_id=artist.id)
    else:
        form = GalleryImageForm()

    return render(request, 'user/upload_gallery_image.html', {'form': form})

@user_required
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user) 
    reviews = Review.objects.filter(user=request.user).select_related('artist')
    context = {
        'user':user,
        'current_user': user_profile,
        'reviews': reviews,
        }  
    return render(request, "user/userdetail.html", context)

@user_required
def user_acc_settings(request):
    user = request.user
    profile = user.userprofile 
    user_form = UserUpdateForm(instance=user)
    profile_form = ProfileForm(instance=profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect(reverse("userprofile", kwargs={"user_id": user.id})) 

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, "user/accountsettings.html", context)

@user_required
def book_time_slot(request, artist_id):
    artist = Makeup.objects.get(id=artist_id)

    # Prevent double booking only if there's an active booking for any artist
    if Booking.objects.filter(user=request.user, status='active', time_slot__isnull=False).exists():
        messages.error(request, "You already have an active booking. Complete or cancel it before booking another.")
        return redirect('bookhistory')

    if request.method == "POST":
        form = BookingForm(artist=artist, data=request.POST)
        if form.is_valid():
            time_slot = form.cleaned_data['time_slot']

            # Check if the selected time slot is already booked by another active booking
            existing_active_booking = Booking.objects.filter(time_slot=time_slot, status='active').exists()
            if existing_active_booking:
                messages.error(request, "This time slot has already been booked.")
                return redirect('booking', artist_id=artist_id)

            # Mark the time slot as booked
            time_slot.is_booked = True
            time_slot.save()

            # Create a new active booking
            Booking.objects.create(
                user=request.user,
                artist=artist,
                time_slot=time_slot,
                status='active'
            )
            message = f"{request.user.username} has booked you for {time_slot.date} at {time_slot.start_time}."
            create_notification(artist, message)

            messages.success(request, f"You have successfully booked a slot on {time_slot.date} at {time_slot.start_time}.")
            return redirect('bookhistory')
    else:
        form = BookingForm(artist=artist)

    return render(request, 'user/booking.html', {'form': form, 'artist': artist})

@user_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at').select_related('time_slot')
    updated_bookings = []
    current_time = now()

    for booking in bookings:
        if not booking.time_slot:
            continue  # skip if related TimeSlot doesn't exist

        try:
            start_dt = datetime.combine(booking.time_slot.date, booking.time_slot.start_time)
            end_dt = datetime.combine(booking.time_slot.date, booking.time_slot.end_time)

            if is_naive(start_dt):
                start_dt = make_aware(start_dt)
            if is_naive(end_dt):
                end_dt = make_aware(end_dt)

            booking.can_cancel = booking.status == 'active' and start_dt > current_time
            booking.can_complete = booking.status == 'active' and start_dt <= current_time < end_dt
            if end_dt < current_time and booking.status == 'active':
                booking.status = 'completed'
                booking.save()


            updated_bookings.append(booking)
        except Exception as e:
            print(f"Error processing booking {booking.id}: {e}")
            continue

    return render(request, 'user/bookhistory.html', {'bookings': updated_bookings,})


@user_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if not booking.time_slot:
        messages.error(request, "This booking no longer has an associated time slot.")
        return redirect('bookhistory')

    slot_datetime = datetime.combine(booking.time_slot.date, booking.time_slot.start_time)

    if is_naive(slot_datetime):
        slot_datetime = make_aware(slot_datetime)

    if slot_datetime > now():
        booking.status = 'cancelled'
        booking.save()

        booking.time_slot.is_booked = False
        booking.time_slot.save()
        message = f"{request.user.username} has cancelled the booking for {booking.time_slot.date} at {booking.time_slot.start_time}."
        create_notification(booking.artist, message)

        messages.success(request, "Your booking has been cancelled and the slot is now available.")
    else:
        messages.error(request, "This booking has already started or passed and cannot be cancelled.")

    return redirect('bookhistory')




@user_required
def complete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if not booking.time_slot:
        messages.error(request, "This booking no longer has an associated time slot.")
        return redirect('bookhistory')

    start_datetime = datetime.combine(booking.time_slot.date, booking.time_slot.start_time)
    
    # Make sure start_datetime is timezone-aware
    if is_naive(start_datetime):
        start_datetime = make_aware(start_datetime)

    current_time = timezone.now()  # timezone-aware now() as per Django's timezone support

    # Ensure current_time is timezone-aware, if not, make it aware
    if is_naive(current_time):
        current_time = make_aware(current_time)

    # Debugging logs to check the actual datetime values
    print("Start datetime:", start_datetime)
    print("Current time:", current_time)

    if booking.status == 'active' and start_datetime <= current_time:
        print("Updating booking status to completed.")
        booking.status = 'completed'
        booking.save()
        message = f"{request.user.username} has marked the booking for {booking.time_slot.date} at {booking.time_slot.start_time} as completed."
        create_notification(booking.artist, message)
        messages.success(request, "Your booking has been marked as completed.")
    else:
        messages.error(request, "You can only mark a booking as completed after its start time.")

    return redirect('bookhistory')



@user_required
def submit_review(request, artist_id):
    artist = get_object_or_404(Makeup, id=artist_id)
    
    try:
        existing_review = Review.objects.get(user=request.user, artist=artist)
    except Review.DoesNotExist:
        existing_review = None

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.artist = artist
            review.save()
            messages.success(request, "Your review has been published.")
            return redirect('artistDetail', artist_id=artist.id)
        else:
            print("Form errors:", form.errors)
            messages.error(request, "There was an error with your review.")
    else:
        form = ReviewForm(instance=existing_review)

    context = {
        'form': form,
        'artist': artist,
        'existing_review': existing_review 
    }
    return render(request, 'user/submit_review.html', context)


