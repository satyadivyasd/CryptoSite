from django.contrib import admin
from .models import Currency, StockData, Payment, Profile,UserProfile

# Import the Currency model from your models.py file

# Register the Currency model with the admin site
admin.site.register(Currency)
admin.site.register(StockData)
admin.site.register(Profile)
admin.site.register(Payment)