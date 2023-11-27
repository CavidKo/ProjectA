from rest_framework import generics

from .serializers import *
from core.models import *


class BlogList(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = GetBlogSerializer


class ClothesList(generics.ListCreateAPIView):
    queryset = Clothes.objects.filter(active=True)
    serializer_class = GetClothesSerializer
