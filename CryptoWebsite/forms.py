from django import forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites import requests
import requests


from .models import UserProfile
class DateForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

# forms.py in your app


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']
class PaymentForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2, required=True)
    card_number = forms.CharField(label='Card Number', max_length=16, required=True)
    expiration_date = forms.CharField(label='Expiration Date', max_length=5, required=True)
    cvv = forms.CharField(label='CVV', max_length=3, required=True)

    # Fetch cryptocurrency options from the CoinMarketCap API
    api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    api_key = '3ebb690c-aa21-4b14-bcd7-c84b1b48420e'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    params = {
        'start': '1',
        'convert': 'USD',  # You can adjust the convert parameter based on your requirements
    }
    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        cryptocurrencies = [(crypto['symbol'], crypto['name']) for crypto in data['data']]
    else:
        # Provide default cryptocurrency options if API request fails
        cryptocurrencies = [('BTC', 'Bitcoin'), ('ETH', 'Ethereum'), ('XRP', 'Ripple')]

    cryptocurrency = forms.ChoiceField(label='Cryptocurrency', choices=cryptocurrencies, required=True)
