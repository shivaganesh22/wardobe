# myapp/middleware.py
from .models import Profile

class ProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                request.profile = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                request.profile = None
        response = self.get_response(request)
        return response
from django.shortcuts import redirect
from django.urls import reverse

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is trying to access the admin page
        if request.path.startswith(reverse('admin:index')):
            # Redirect non-superusers to a custom page
            if not request.user.is_superuser:
                return redirect('/not-authorized/')  # Replace with your custom URL
        return self.get_response(request)
