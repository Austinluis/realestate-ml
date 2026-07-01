from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import User
from properties.models import Property
from predictions.models import Prediction

def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        login_data = request.POST.copy()
        if login_data.get('email') and not login_data.get('identifier'):
            login_data['identifier'] = login_data['email']
        form = LoginForm(login_data)
        if form.is_valid():
            identifier = form.cleaned_data['identifier'].strip()
            password = form.cleaned_data['password']
            auth_identifier = identifier
            if '@' not in identifier:
                matched_user = User.objects.filter(username__iexact=identifier).first()
                if matched_user:
                    auth_identifier = matched_user.email
            user = authenticate(request, username=auth_identifier, password=password)
            if user:
                login(request, user)
                return redirect(request.GET.get('next', 'dashboard'))
            else:
                messages.error(request, 'Invalid username/email or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    property_count = Property.objects.filter(owner=request.user).count()
    prediction_count = Prediction.objects.filter(user=request.user).count()
    recent_properties = Property.objects.filter(owner=request.user).order_by('-created_at')[:5]
    recent_predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'dashboard/index.html', {
        'property_count': property_count,
        'prediction_count': prediction_count,
        'recent_properties': recent_properties,
        'recent_predictions': recent_predictions,
    })
