
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import RideRequestForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Ride, Ridesharer
from django.views.generic.edit import UpdateView
from .forms import RideSearchForm
from django.utils.dateparse import parse_datetime
from users.models import Driver

from django.core.mail import send_mail

from django.db.models import Q
import logging





@login_required
def ride_home(request):
    # Add your logic here
    return render(request, 'ride_home.html')


class RideRequestView(LoginRequiredMixin, CreateView):
    model = Ride
    form_class = RideRequestForm
    template_name = 'ride_request.html'
    success_url = reverse_lazy('ride_home')  # Redirect to 'ride_home' after a successful request

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Set the owner of the ride to the current user
        return super().form_valid(form)



# @login_required
# def ride_request(request):
#     # Add your logic here
#     return render(request, 'ride_request.html')




@login_required
def view_rides(request):
    # Fetch rides where the current user is the owner
    owned_rides = Ride.objects.filter(owner=request.user)

    # Fetch rides where the current user is a sharer
    shared_rides_ids = Ridesharer.objects.filter(sharer=request.user).values_list('ride', flat=True)
    shared_rides = Ride.objects.filter(id__in=shared_rides_ids)

    context = {
        'owned_rides': owned_rides,
        'shared_rides': shared_rides,
    }
    return render(request, 'view_rides.html', context)



class RideEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    form_class = RideRequestForm
    template_name = 'ride_edit.html'
    context_object_name = 'ride'
    success_url = reverse_lazy('view_rides')  # Redirect to 'ride_home' after a successful request

    # def get_success_url(self):
    #     return reverse_lazy('ride_home', kwargs={'pk': self.object.pk})

    def test_func(self):
        ride = self.get_object()
        return ride.owner == self.request.user and ride.status != Ride.RideStatus.CONFIRMED

    def form_valid(self, form):
        if form.instance.status == Ride.RideStatus.CONFIRMED:
            form.add_error(None, 'Cannot edit a confirmed ride.')
            return self.form_invalid(form)
        return super().form_valid(form)



@login_required
def join_ride(request):
    # Add your logic here
    return render(request, 'join_ride.html')


# views.py
@login_required
def search_and_join_ride(request):
    

    search_form = RideSearchForm(request.POST or None)
    rides = Ride.objects.none()

    if request.method == 'POST' and 'search' in request.POST and search_form.is_valid():
        # Filtering logic for rides
        destination = search_form.cleaned_data['destination']
        earliest_arrive = search_form.cleaned_data['earliest_arrive']
        latest_arrive = search_form.cleaned_data['latest_arrive']
        passenger_num = search_form.cleaned_data['passenger_num']
        
        rides = Ride.objects.filter(
            status='OPEN',
            destination=destination,
            arrive_time__gte=earliest_arrive,
            arrive_time__lte=latest_arrive,
        )

    return render(request, 'search_and_join_ride.html', {'form': search_form, 'rides': rides})

# @login_required
# def search_rides(request):
#     search_form = RideSearchForm(request.POST or None)
#     rides = Ride.objects.none()

#     if request.method == 'POST' and search_form.is_valid():
#         destination = search_form.cleaned_data['destination']
#         earliest_arrive = search_form.cleaned_data['earliest_arrive']
#         latest_arrive = search_form.cleaned_data['latest_arrive']
#         passenger_num = search_form.cleaned_data['passenger_num']

#         rides = Ride.objects.filter(
#             status='OPEN',
#             destination=destination,
#             arrive_time__gte=earliest_arrive,
#             arrive_time__lte=latest_arrive
#         )

#     return render(request, 'search_rides.html', {'form': search_form, 'rides': rides})


# @login_required
# def join_ride(request, ride_id):
#     if request.method == 'POST':
        
#         ride = Ride.objects.get(id=ride_id)
#         Ridesharer.objects.create(ride=ride, sharer=request.user)  # Assuming other fields are handled
#         return redirect('some_success_view')  # Redirect to a success or confirmation page

#     return redirect('search_rides')  # Redirect back to the search page if not a POST request


# @login_required
# def search_rides(request):
#     search_form = RideSearchForm(request.POST or None)
#     rides = Ride.objects.none()

#     if request.method == 'POST' and search_form.is_valid():
#         # Save form data to session for later use in join_ride
#         request.session['search_data'] = search_form.cleaned_data

#         destination = search_form.cleaned_data['destination']
#         earliest_arrive = search_form.cleaned_data['earliest_arrive']
#         latest_arrive = search_form.cleaned_data['latest_arrive']

#         rides = Ride.objects.filter(
#             status='OPEN',
#             destination=destination,
#             arrive_time__gte=earliest_arrive,
#             arrive_time__lte=latest_arrive
#         )

#     return render(request, 'search_rides.html', {'form': search_form, 'rides': rides})


# @login_required
# def join_ride(request, ride_id):
#     if request.method == 'POST':
#         ride = Ride.objects.get(id=ride_id)
        
#         # Retrieve search form data from the session
#         search_data = request.session.get('search_data', {})
#         earliest_arrive = parse_datetime(search_data.get('earliest_arrive')) if search_data.get('earliest_arrive') else None
#         latest_arrive = parse_datetime(search_data.get('latest_arrive')) if search_data.get('latest_arrive') else None

#         passenger_num =  search_data.get('passenger_num')

#         Ridesharer.objects.create(ride, request.user, earliest_arrive_date, latest_arrive_date, passenger_num)
        
#         return redirect('view_rides')

#     return redirect('search_rides')



@login_required
def search_rides(request):
    search_form = RideSearchForm(request.POST or None)
    rides = Ride.objects.none()

    if request.method == 'POST' and search_form.is_valid():
        # Convert datetime objects to strings for JSON serialization
        search_data = {
            'destination': search_form.cleaned_data['destination'],
            'earliest_arrive': search_form.cleaned_data['earliest_arrive'].isoformat() if search_form.cleaned_data['earliest_arrive'] else None,
            'latest_arrive': search_form.cleaned_data['latest_arrive'].isoformat() if search_form.cleaned_data['latest_arrive'] else None,
            'passenger_num': search_form.cleaned_data['passenger_num']
        }

        request.session['search_data'] = search_data

        destination = search_form.cleaned_data['destination']
        earliest_arrive = search_form.cleaned_data['earliest_arrive']
        latest_arrive = search_form.cleaned_data['latest_arrive']

        rides = Ride.objects.filter(
            status='OPEN',
            destination=destination,
            arrive_time__gte=earliest_arrive,
            arrive_time__lte=latest_arrive
        )

    return render(request, 'search_rides.html', {'form': search_form, 'rides': rides})

@login_required
def join_ride(request, ride_id):
    if request.method == 'POST':
        ride = Ride.objects.get(id=ride_id)
        search_data = request.session.get('search_data', {})

        earliest_arrive = parse_datetime(search_data.get('earliest_arrive')) if search_data.get('earliest_arrive') else None
        latest_arrive = parse_datetime(search_data.get('latest_arrive')) if search_data.get('latest_arrive') else None
        passenger_num = search_data.get('passenger_num')

        # Assuming Ridesharer has fields for earliest_arrive_date and latest_arrive_date
        Ridesharer.objects.create(ride=ride, sharer=request.user, earliest_arrive_date=earliest_arrive, latest_arrive_date=latest_arrive, passenger_num=passenger_num)
        # update ride
        ride.current_passengers_num +=  passenger_num
        ride.save() 
        
        return redirect('view_rides')

    return redirect('search_rides')



@login_required
def offer_ride(request):
    # Check if the user is a driver
    if Driver.objects.filter(user=request.user).exists():
        return redirect('driver_home')
    else:
        return redirect('user_info')

@login_required
def driver_home(request):
    return render(request, 'driver_home.html')


# @login_required
# def offer_ride(request):
#     # Add your logic here
#     return render(request, 'offer_ride.html')

# @login_required
# def ride_search(request):
#     # Add your logic here
#     return render(request, 'ride_search.html')



# @login_required
# def driver_ride_search(request):
#     try:
#         driver = Driver.objects.get(user=request.user)
#         rides = Ride.objects.filter(
#             status=Ride.RideStatus.OPEN,
#             vehicle_type__icontains=driver.vehicle_type,
#             special_request__icontains=driver.special_vehicle_info,
#             current_passengers_num__lte=driver.max_capacity
#         )
#     except Driver.DoesNotExist:
#         rides = Ride.objects.none()  # No rides to show if the user is not a driver

#     return render(request, 'driver_ride_search.html', {'rides': rides})

# @login_required
# def driver_ride_search(request):
#     # Start with no rides
#     rides = Ride.objects.none()

#     # Check if the user is a driver
#     try:
#         driver = Driver.objects.get(user=request.user)

#         # Get all open rides
#         open_rides = Ride.objects.filter(status=Ride.RideStatus.OPEN)

#         # Filter rides that either have no vehicle_type requirement or match the driver's vehicle type
#         rides = open_rides.filter(
#             current_passengers_num__lte=driver.max_capacity
#         ).filter(
#             # Using Q objects to combine queries with OR
#             Q(vehicle_type='') | Q(vehicle_type__iexact=driver.vehicle_type),
#             # Matching special requests
#             Q(special_request='') | Q(special_request__icontains=driver.special_vehicle_info)
#         )

#     except Driver.DoesNotExist:
#         # If the user is not a driver, show no rides
#         pass

#     return render(request, 'driver_ride_search.html', {'rides': rides})

@login_required
def driver_ride_search(request):
    try:
        driver = Driver.objects.get(user=request.user)

        # Exclude rides where the driver is the owner or a sharer
        excluded_ride_ids = set(
            Ride.objects.filter(owner=driver.user).values_list('id', flat=True)
        )
        excluded_ride_ids.update(
            Ridesharer.objects.filter(sharer=driver.user).values_list('ride_id', flat=True)
        )

        # Filter open rides that are not in the excluded list
        rides = Ride.objects.filter(
            status=Ride.RideStatus.OPEN
        ).exclude(
            id__in=excluded_ride_ids
        ).filter(
            current_passengers_num__lte=driver.max_capacity,
            vehicle_type__in=['', driver.vehicle_type],
            special_request__in=['', driver.special_vehicle_info]
        )

    except Driver.DoesNotExist:
        rides = Ride.objects.none()  # No rides to show if the user is not a driver

    return render(request, 'driver_ride_search.html', {'rides': rides})




@login_required
def claim_ride(request, ride_id):
    try:
        driver = Driver.objects.get(user=request.user)
        ride = Ride.objects.get(id=ride_id, status=Ride.RideStatus.OPEN)

        ride.driver = driver
        ride.status = Ride.RideStatus.CONFIRMED
        ride.save()

        # Send notification about claiming the ride
        send_ride_notification_email(ride, 'Ride Claimed Notification')

        # Redirect to a success page or driver's dashboard
        return redirect('view_confirmed_rides')
    except (Ride.DoesNotExist, Driver.DoesNotExist):
        # Handle exceptions or redirect to an error page
        return redirect('error_page')

# def send_ride_notification_email(ride, subject):
#     try:
#         recipient_list = [ride.owner.email] + [sharer.sharer.email for sharer in ride.sharers.all()]
#         message = f"Notification for ride to {ride.destination} on {ride.arrive_time}: {subject}"
#         #send_mail(subject, message, 'from@example.com', recipient_list)
#         send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
#     except Exception as e:  # Catch all exceptions related to send_mail
#         return redirect('error_page')
    
logger = logging.getLogger(__name__)

def send_ride_notification_email(ride, subject):
    try:
        recipient_list = [ride.owner.email] + [sharer.sharer.email for sharer in ride.sharers.all()]
        message = f"Notification for ride to {ride.destination} on {ride.arrive_time}: {subject}"
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    except Exception as e:  # Catch all exceptions related to send_mail
        logger.error(f"Failed to send email notification: {e}")
    

# @login_required
# def view_confirmed_rides(request):
#     # Add your logic here
#     return render(request, 'view_confirmed_rides.html')


@login_required
def view_confirmed_rides(request):
    driver = get_object_or_404(Driver, user=request.user)
    rides = Ride.objects.filter(driver=driver, status=Ride.RideStatus.CONFIRMED)

    return render(request, 'view_confirmed_rides.html', {'rides': rides})


@login_required
def complete_ride(request, ride_id):
    if request.method == 'POST':
        ride = get_object_or_404(Ride, id=ride_id, driver__user=request.user)
        ride.status = Ride.RideStatus.COMPLETE
        ride.save()

        # Redirect to the driver's confirmed rides page
        return redirect('driver_home')

    # Redirect back if not a POST request
    return redirect('view_confirmed_rides')
