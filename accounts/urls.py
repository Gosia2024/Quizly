from django.urls import path
from accounts.views import logout_user, refresh_token,  register_user
from accounts.views import login_user

urlpatterns = [
    path('register/', register_user),
    path('login/', login_user),
    path('logout/', logout_user),
    path('token/refresh/', refresh_token),

]  
