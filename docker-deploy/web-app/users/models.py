from django.db import models
from django.contrib.auth.models import User  # Import the User model

# Create your models here.
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    license_number = models.CharField(max_length=10, blank=True)
    vehicle_type = models.CharField(max_length=20, blank=True)
    max_capacity = models.PositiveIntegerField()
    special_vehicle_info = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.license_number}'
