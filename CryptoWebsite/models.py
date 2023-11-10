from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
class Currency(models.Model):
    name=models.CharField(max_length=100)
    code=models.CharField(max_length=100)
    def __str__(self):
        return self.code
class StockData(models.Model):
    stock = models.IntegerField()
    stock_rate = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return  self.date.strftime('%B %Y')


