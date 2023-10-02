from django.urls import path
from core.views import index, contact

urlpatterns = [
    path('home/', index, name='home'),
    path('contact/', contact, name='contact'),
]