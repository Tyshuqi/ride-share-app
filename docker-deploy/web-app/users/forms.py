from django import forms
from .models import Driver
from django.contrib.auth.models import User

class DriverRegistrationForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['license_number', 'vehicle_type', 'max_capacity', 'special_vehicle_info']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
        
        
class DriverUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['license_number', 'vehicle_type', 'max_capacity', 'special_vehicle_info']
        
