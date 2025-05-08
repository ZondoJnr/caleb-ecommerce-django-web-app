from django.shortcuts import redirect
from .models import Profile

def vendor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.role == 'vendor':
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper

def buyer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.role == 'buyer':
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper
