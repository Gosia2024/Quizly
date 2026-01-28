from django.urls import path

from accounts.views import login_user

urlpatterns = [
    path('login/', login_user),
]
