"""
URL configuration for the accounts app.

This module routes authentication-related requests to their respective views:
- User registration
- Login/Logout (JWT/Session based)
- Token management
"""
from django.urls import path
from accounts.views import logout_user, refresh_token,  register_user
from accounts.views import login_user

urlpatterns = [
    path('register/', register_user, name="register"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('token/refresh/', refresh_token, name="token_refresh"),
]