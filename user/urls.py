from user.views import user_login, register, user_logout
from core.views import index
from django.urls import path


urlpatterns = [
    path('', user_login, name='login'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('cozastore/home/', index, name='home'),
    path('logout', user_logout, name='logout'),
]