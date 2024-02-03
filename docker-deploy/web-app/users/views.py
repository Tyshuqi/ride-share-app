from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from .forms import DriverRegistrationForm, UserUpdateForm, DriverUpdateForm
from .models import Driver
from django.contrib import messages

from .forms import CustomUserCreationForm


def home(request):
    return render(request, 'index.html')




def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            user.email = form.cleaned_data.get('email')
            user.save()
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def user_info(request):
    user = request.user
    try:
        driver = user.driver
    except Driver.DoesNotExist:
        driver = None

    context = {
        'user': user,
        'driver': driver
    }
    return render(request, 'user_info.html', context)


@login_required
def register_driver(request):
    user = request.user
    if Driver.objects.filter(user=user).exists():
        # messages.error(request, "You are already registered as a driver.")
        return redirect('user_info')  

    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.user = user
            driver.save()
            # messages.success(request, "You have been successfully registered as a driver.")
            return redirect('user_info')  
    else:
        form = DriverRegistrationForm()

    return render(request, 'register_driver.html', {'form': form})



@login_required
def update_user_info(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('user_info')

    else:
        user_form = UserUpdateForm(instance=request.user)

    context = {'user_form': user_form}
    return render(request, 'update_user_info.html', context)


@login_required
def update_driver_info(request):
    try:
        driver = request.user.driver
    except Driver.DoesNotExist:
        driver = None

    if request.method == 'POST' and driver is not None:
        driver_form = DriverUpdateForm(request.POST, instance=driver)
        if driver_form.is_valid():
            driver_form.save()
            
            return redirect('user_info')

    else:
        driver_form = DriverUpdateForm(instance=driver)

    context = {'driver_form': driver_form}
    return render(request, 'update_driver_info.html', context)