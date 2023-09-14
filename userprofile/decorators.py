from functools import wraps
from django.shortcuts import redirect
from .models import Profile  # Replace with actual import

def check_profile_exists(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not Profile.objects.filter(user=user).exists():  # Change 'person' to the actual OneToOneField name
            return redirect('/userprofile')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
