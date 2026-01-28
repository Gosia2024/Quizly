from django.urls import path
from accounts.views import register_user
from accounts.views import login_user

urlpatterns = [
    path('register/', register_user),
    path('login/', login_user),
]
