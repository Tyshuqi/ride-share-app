from django import forms
from .models import Driver

class DriverRegistrationForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['license_number', 'vehicle_type', 'max_capacity', 'special_vehicle_info']
