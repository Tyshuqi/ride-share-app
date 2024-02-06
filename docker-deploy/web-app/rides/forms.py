
from django import forms
from .models import Ride, Ridesharer

class RideRequestForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['destination', 'arrive_time', 'current_passengers_num', 'vehicle_type', 'can_be_shared', 'special_request']
        widgets = {
            'arrive_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }



# class RideSearchForm(forms.Form):
#     destination = forms.CharField(required=False)
#     earliest_arrive = forms.DateTimeField(required=False)
#     latest_arrive = forms.DateTimeField(required=False)
#     passenger_num = forms.IntegerField(required=False, min_value=1)


class RideSearchForm(forms.Form):
    #2.5 delete required=False
    destination = forms.CharField()
    earliest_arrive = forms.DateTimeField(
        #required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']  # Match the format to the 'datetime-local' input
    )
    latest_arrive = forms.DateTimeField(
        #required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']  # Match the format to the 'datetime-local' input
    )
    passenger_num = forms.IntegerField(min_value=1)
    #2.5 new add for sharer special info
    special_request = forms.CharField(required=False) 
    
    
    
    
#2.5 add
class EditRideSharerForm(forms.ModelForm):
    class Meta:
        model = Ridesharer
        fields = ['passenger_num']