from django.urls import path
from .views import ride_home, offer_ride, view_rides, search_rides, join_ride, RideRequestView, RideEditView, search_and_join_ride

urlpatterns = [
    # ... other patterns ...
    path('ride-home/', ride_home, name='ride_home'),
    path('offer-ride/', offer_ride, name='offer_ride'),
    #path('ride-request/', ride_request, name='ride_request'),
    path('ride-request/', RideRequestView.as_view(), name='ride_request'),
    path('view-rides/', view_rides, name='view_rides'),
    #path('join-ride/',join_ride, name='join_ride'),
    # path('search-and-join-ride/', search_and_join_ride, name='search_and_join_ride'),
    path('search-rides/', search_rides, name='search_rides'),
    path('join-ride/<int:ride_id>/', join_ride, name='join_ride'),
    path('ride/<int:pk>/edit/', RideEditView.as_view(), name='ride_edit'),
]

