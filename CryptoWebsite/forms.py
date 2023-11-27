
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ContactMessage, Profile, PaymentHistory
import requests


from .models import Feedback



class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',]



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = 'first_name','last_name','phone_no','date_of_birth','profile_image'

        def __init__(self, *args, **kwargs):
            super(UserProfileForm, self).__init__(*args, **kwargs)
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

class SellCryptoForm(forms.Form):
    quantity = forms.DecimalField(max_digits=20, decimal_places=0)
    price_per_unit = forms.DecimalField(max_digits=20, decimal_places=2)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message', 'cryptocurrency_experience', 'platform_satisfaction', 'security_confidence', 'future_expectations']

class MakePaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentHistory
        fields = ['stock_name', 'quantity_purchased', 'purchased_currency', 'purchase_price_per_unit',
                  'payment_method']
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = 'first_name','last_name', 'phone_no','date_of_birth','profile_image'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }