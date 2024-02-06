from django.urls import path
from .views import ride_home, offer_ride, view_rides, search_rides, join_ride, RideRequestView, RideEditView
from .views import driver_home, view_confirmed_rides, driver_ride_search, claim_ride, complete_ride, owner_ride_details, sharer_ride_details, driver_ride_details, error_page
#2.5 add
from .views import sharer_ride_edit

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
    path('owner-ride-details/<int:ride_id>/', owner_ride_details, name='owner_ride_details'),
    path('sharer-ride-details/<int:ride_id>/', sharer_ride_details, name='sharer_ride_details'),
        
    #path('offer-ride/', offer_ride, name='offer_ride'),
    path('driver-home/', driver_home, name='driver_home'),
    path('driver-ride-search/', driver_ride_search, name='driver_ride_search'),
    path('view-confirmed-rides/', view_confirmed_rides, name='view_confirmed_rides'),
    path('rides/claim/<int:ride_id>/', claim_ride, name='claim_ride'),
    path('driver-error/', error_page, name='error_page'),
    
    path('driver-ride-details/<int:ride_id>/', driver_ride_details, name='driver_ride_details'),
    #path('driver-rides/', view_driver_rides, name='view_driver_rides'),
    path('complete-ride/<int:ride_id>/', complete_ride, name='complete_ride'),
    
    
    #2.5 add
    path('edit-sharer/<int:ride_id>/', sharer_ride_edit, name='edit_sharer'),
    
]

