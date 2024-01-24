from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Import your app's views

urlpatterns = [
    # ... your other url patterns ...

    # Login and Logout URLs using Django's built-in views
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    # URL for account creation
    path('signup/', views.signup, name='signup'),
]
