from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  
from .views import register_driver, update_user_info, update_driver_info 
from .views import home, user_info

urlpatterns = [

    #path('', base, name='public_home'),
    path('', home, name='home'),
    # Login and Logout URLs using Django's built-in views
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),


    path('signup/', views.signup, name='signup'),
    

    path('register-driver/', register_driver, name='register_driver'),
    

    path('user-info/', user_info, name='user_info'),
    
    path('update-user-info/', update_user_info, name='update_user_info'),
    path('update-driver-info/', update_driver_info, name='update_driver_info'),
   

]
