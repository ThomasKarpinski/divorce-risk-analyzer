from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from rest_framework.authtoken.models import Token
from django.conf import settings
import requests

User = get_user_model()

def validate_turnstile(token):
    """Verify Cloudflare Turnstile token."""
    if not token:
        return False
    
    response = requests.post(
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        data={
            'secret': settings.TURNSTILE_SECRET_KEY,
            'response': token,
        },
        timeout=5
    )
    result = response.json()
    return result.get('success', False)

def register_view(request):
    if request.method == 'POST':
        # Turnstile Verification
        turnstile_token = request.POST.get('cf-turnstile-response')
        if not validate_turnstile(turnstile_token):
            messages.error(request, 'Invalid captcha. Please try again.')
            return render(request, 'register.html')

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        birthdate = request.POST.get('birthdate')
        gender = request.POST.get('gender')
        education = request.POST.get('education')
        residence = request.POST.get('residence')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'register.html')

        user = User.objects.create_user(
            username=username, 
            email=email,
            password=password,
            birthdate=birthdate,
            gender=gender,
            education=education,
            residence=residence
        )
        Token.objects.create(user=user)
        
        login(request, user)
        return redirect('home')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        # Turnstile Verification
        turnstile_token = request.POST.get('cf-turnstile-response')
        if not validate_turnstile(turnstile_token):
            messages.error(request, 'Invalid captcha. Please try again.')
            return render(request, 'login.html')

        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            
    return render(request, 'login.html')