from django.db import models
from django.contrib.auth.models import AbstractUser
from collections.abc import Iterable


# Create your models here.

class MyUser(AbstractUser):
    address = models.CharField(max_length=250)
    birth_date = models.DateField(null=True, blank=True)
    picture = models.ImageField(upload_to='users', blank=True)

    