from django import forms
from .models import Driver
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


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
        
