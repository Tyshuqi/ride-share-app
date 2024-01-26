from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.
from users.models import Driver  # Import the Driver model from the users app


class Ride(models.Model):
    class RideStatus(models.TextChoices):
        OPEN = 'OPEN', _('Open')
        CONFIRMED = 'CONFIRMED', _('Confirmed')
        COMPLETE = 'COMPLETE', _('Complete')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_rides')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='driven_rides')
    destination = models.CharField(max_length=512)
    arrive_time = models.DateTimeField()
    current_passengers_num = models.PositiveIntegerField(default=1)
    vehicle_type = models.CharField(max_length=128, blank=True)
    special_request = models.TextField(blank=True)
    can_be_shared = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=RideStatus.choices, default=RideStatus.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.destination} - {self.arrive_time}'


class Ridesharer(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='sharers')
    sharer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_rides')
    earliest_arrive_date = models.DateTimeField()
    latest_arrive_date = models.DateTimeField()
    passenger_num = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.sharer.username} - Request for {self.ride.destination}'




