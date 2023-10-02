from django.urls import path
from core.views import index, contact, blog

urlpatterns = [
    path('home/', index, name='home'),
    path('contact/', contact, name='contact'),
    path('blog/', blog, name='blog'),
]