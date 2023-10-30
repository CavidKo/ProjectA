from django.urls import path
from core.views import index, contact, blog, product, about, features

urlpatterns = [
    # path('', index, name='home'),
    path('home/', index, name='home'),
    path('contact/', contact, name='contact'),
    path('blog/', blog, name='blog'),
    path('shop/', product, name='shop'),
    path('about/', about, name='about'),
    path('features/', features, name='features'),
]