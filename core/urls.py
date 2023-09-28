from django.urls import path
from core.views import index

urlpatterns = [
    path('home/', index, name='home'),
]