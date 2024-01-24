#from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic


from django.contrib.auth.decorators import login_required
from .forms import DriverRegistrationForm

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})




@login_required
def register_driver(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.user = request.user
            driver.save()
            return redirect('some_view')  # Redirect to a success page or profile page
    else:
        form = DriverRegistrationForm()
    return render(request, 'register_driver.html', {'form': form})

