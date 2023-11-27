
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import uuid

class Currency(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    def __str__(self):
        return self.code
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

    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    date_of_birth = models.DateField(null=True)
    email = models.EmailField(null=True)
    phone_no = models.IntegerField(null=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True)
    def __str__(self):
        return self.first_name

class PaymentHistory(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('OL', 'ONLINE'),
        ('CARD', 'CARD'),
    ]

    STATUS_CHOICES = [
        ('A', 'ACTIVE'),
        ('I', 'INACTIVE'),
    ]

    TRANSACTION_TYPE = [
        ('B', 'BUY'),
        ('S', 'SELL'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(default=timezone.now)
    transaction_id = models.CharField(
        max_length=8,
        blank=True,
        null=True,
        unique=True)

    stock_name = models.CharField(max_length=100)
    quantity_purchased = models.IntegerField(default=1)
    updated_quantity = models.IntegerField(default=0)
    purchased_currency = models.CharField(max_length=3, default='CAD')
    purchase_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    total_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    updated_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(
        max_length=4,
        choices=PAYMENT_METHOD_CHOICES,
        default='OL'
    )

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE, default='B')

    status = models.CharField(
        max_length=4,
        choices=STATUS_CHOICES,
        default='A'
    )

    def __str__(self):
        return self.stock_name

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = uuid.uuid4().hex[:8]
        self.total_purchase_amount = self.quantity_purchased * self.purchase_price_per_unit
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-payment_date']




