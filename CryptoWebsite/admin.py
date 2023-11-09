from django.contrib import admin
from .models import Currency  # Import the Currency model from your models.py file

# Register the Currency model with the admin site
admin.site.register(Currency)
