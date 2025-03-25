from django.shortcuts import redirect
# creating a decorator in order to manage access between users
from functools import wraps

#giving access to only admin in adminpage and not normal users if they try to access in
def admin_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_function(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper_function

def artist_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                if request.user.userprofile.is_artist:
                    return view_func(request, *args, **kwargs)
            except AttributeError:
                pass
        return redirect('home')  # Redirect non-artists to home
    return wrapper


def user_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                if not request.user.userprofile.is_artist:
                    return view_func(request, *args, **kwargs)
            except AttributeError:
                pass
        return redirect('login')  # Redirect artists to home
    return wrapper