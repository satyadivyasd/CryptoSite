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
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2)
    change_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    volume_24h = models.DecimalField(max_digits=20, decimal_places=2)
    lasthour = models.DecimalField(max_digits=10, decimal_places=2)
    volume_change_24h = models.DecimalField(max_digits=20, decimal_places=2)
    last24h = models.DecimalField(max_digits=10, decimal_places=2)
    week = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DecimalField(max_digits=10, decimal_places=2)
    TwoMonths= models.DecimalField(max_digits=10, decimal_places=2)
    ThreeMonths = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    # Add other fields as needed
# models.py


