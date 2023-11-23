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


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    transaction_id = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.amount} {self.currency}'

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # New fields related to cryptocurrency feedback
    cryptocurrency_experience = models.IntegerField(choices=[
        (1, 'Novice'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
    ], default=1)
    platform_satisfaction = models.IntegerField(choices=[
        (1, 'Not satisfied'),
        (2, 'Satisfied'),
        (3, 'Very satisfied'),
    ], default=2)
    security_confidence = models.IntegerField(choices=[
        (1, 'Low'),
        (2, 'Moderate'),
        (3, 'High'),
    ], default=2)
    future_expectations = models.TextField(blank=True, null=True)
    # Add more fields as needed