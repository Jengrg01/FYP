from django.shortcuts import redirect
# creating a decorator in order to manage access between users

#giving access to only admin in adminpage and not normal users if they try to access in
def admin_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_function(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper_function