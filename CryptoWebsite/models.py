from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.code


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
class StockData(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=10)
    timestamp = models.DateTimeField()
    price = models.FloatField()

    def __str__(self):
        return self.name

    # Add other fields as needed
# models.py


