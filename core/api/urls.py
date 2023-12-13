from .views import *
from django.urls import path

urlpatterns = [
    path('blog/', BlogList.as_view(), name='blog'),
    path('product/', ClothesList.as_view(), name='product'),
    # path('whishlist/', AddToWhishList.as_view(), name='whish'),
]