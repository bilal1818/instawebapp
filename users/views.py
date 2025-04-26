from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser

# Create your views here.

def register_view(request):
    """View for user registration (consumers only)"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('core:home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    """View for user login"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                
                # Redirect to appropriate page based on user role
                next_url = request.GET.get('next', 'core:home')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    """View for user logout"""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('core:home')

# Helper function for role-based access control
def creator_required(view_func):
    """Decorator to restrict access to creator users only"""
    decorated_view = user_passes_test(
        lambda u: u.is_authenticated and u.role == 'creator',
        login_url='users:login'
    )(view_func)
    return decorated_view
