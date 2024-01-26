from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Import your app's views
from .views import register_driver, update_user_info, update_driver_info # Import the view here
from .views import home

urlpatterns = [
    # ... your other url patterns ...
    #path('', base, name='public_home'),
    path('', home, name='home'),
    # Login and Logout URLs using Django's built-in views
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    # URL for account creation
    path('signup/', views.signup, name='signup'),
    
    #URL for driver register
    path('register-driver/', views.register_driver, name='register_driver'),
    
    #URL for usrs_info_list
    path('user-info/', views.user_info, name='user_info'),
    
    path('update-user-info/', update_user_info, name='update_user_info'),
    path('update-driver-info/', update_driver_info, name='update_driver_info'),
   

]
