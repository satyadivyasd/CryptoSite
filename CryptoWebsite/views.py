from datetime import datetime, timedelta
from decimal import Decimal
from django.conf import settings

from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
import plotly.express as px
import requests
from django.shortcuts import render


from django.urls import reverse
from .models import StockData, Currency, Payment
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, UserProfileForm, PaymentForm, FeedbackForm, ContactUs


def convert_currency(request, amount, from_currency, to_currency):
    payload = {}
    headers = {
        "apikey": "405iqxjRNuup95vMq52Cv2cGW6d5zONh"
    }
    url = f"https://api.apilayer.com/fixer/convert?to={to_currency}&from={from_currency}&amount={amount}"
    response = requests.request("GET", url, headers=headers, data=payload)
    status_code = response.status_code
    data = response.json()
    converted_amount = data.get('result', None)
    c = Currency.objects.all()
    result = {
        'CONVERSION_AMOUNT': converted_amount,
        'currencies': c,
        'price':amount,
        'STOCK_NAME':settings.STOCK_NAME,
        'CHART':settings.CHART,
        'PREV_CODE':to_currency
    }
    settings.CONVERSION_AMOUNT=converted_amount
    settings.PREV_CODE=from_currency
    if response.status_code == 200:
        return render(request, 'CryptoWebsite/tradeinfo.html', result)


    else:
        return JsonResponse({'success': False, 'error': 'Failed to retrieve data from the API'})


def home(request):
    currencies = Currency.objects.all()
    context={'currencies':currencies}
    return render(request, 'CryptoWebsite/home.html',context)


# Create your views here.
def stockinfo(request, stockname):
    data = StockData.objects.filter(name=stockname).first()
    settings.STOCK_NAME=stockname
    currencies = Currency.objects.all()
    if data:
        # Extract field names and values for the chart
        fields = [field.name for field in StockData._meta.get_fields() if
                  field.name not in ['id', 'name', 'date', 'name', 'price', 'market_cap', 'change_percentage',
                                     'volume_24h', 'volume_change_24h', 'volume_change_24h']]
        values = [getattr(data, field) for field in fields]

        # Create a bar chart with field names on x-axis and values on y-axis
        fig = px.line(
            x=fields,
            y=[values],
            labels={'x': 'Stock Time', 'y': 'Stock Change'},
            title=f"Stock Data for {stockname}",
        )

        fig.update_layout(
            title={
                'font_size': 24,
                'xanchor': 'center',
                'x': 0.5
            }
        )

        chart = fig.to_html()
        settings.CHART=chart
        settings.CONVERSION_AMOUNT=data.price
        settings.STOCK_NAME=stockname
        context = {'CHART': chart,
                   'CONVERSION_AMOUNT': data.price,
                   'STOCK_NAME': stockname,
                   'currencies': currencies,
                   'PREV_CODE':settings.PREV_CODE
                   }
    else:
        context = {
                'chart': None

                   }

    return render(request, 'CryptoWebsite/tradeinfo.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')  # Redirect to login page after successful registration
        else:
            # Capture validation errors and pass them to the template
            user_errors = user_form.errors
            profile_errors = profile_form.errors
            return render(request, 'CryptoWebsite/register.html',
                          {'user_form': user_form, 'profile_form': profile_form, 'user_errors': user_errors,
                           'profile_errors': profile_errors})

    else:
        user_form = RegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'CryptoWebsite/register.html', {'user_form': user_form, 'profile_form': profile_form})

def contactus(request):
    if request.method=='POST':
        contactform=ContactUs(request.POST)
        if contactform.is_valid():
            return ('/home')
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))  # Redirect to the user's account page after login
        else:
            return render(request, 'CryptoWebsite/login.html', {'error': 'Invalid login credentials.'})
    else:
        return render(request, 'CryptoWebsite/login.html')


@login_required
def myaccount(request):
    user_profile = request.user.userprofile

    return render(request, 'CryptoWebsite/userprofile.html', {'user_profile': user_profile})


# def data(request):
#     # CoinMarketCap API endpoint for cryptocurrency listings
#     api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
#     # Add your CoinMarketCap API key here
#     api_key = '3ebb690c-aa21-4b14-bcd7-c84b1b48420e'
#     # Define parameters for the API request
#     params = {
#         'start': '1',
#         'limit': '10',
#         'convert': 'USD'
#     }
#     # Set headers, including the API key
#     headers = {
#         'Accepts': 'application/json',
#         'X-CMC_PRO_API_KEY': api_key,
#     }
#     # Make the API request
#     response = requests.get(api_url, headers=headers, params=params)
#     if response.status_code == 200:
#         # Parse the JSON response
#         data = response.json()
#         # Extract relevant information from the response
#
#         cryptocurrencies = [
#             {
#                 'name': crypto['name'],
#                 'symbol': crypto['symbol'],
#                 'price': '${:,.2f}'.format(crypto['quote']['USD']['price']),
#                 'market_cap': '${:,.2f}'.format(crypto['quote']['USD']['market_cap']),
#                 'change_percentage': '{:.2f}'.format(crypto['quote']['USD']['percent_change_24h']),
#                 'volume_24h': crypto['quote']['USD']['volume_24h'],
#                 "volume_change_24h": crypto['quote']['USD']['volume_change_24h'],
#                 "percent_change_1h": crypto['quote']['USD']['percent_change_1h'],
#                 "percent_change_24h": crypto['quote']['USD']['percent_change_24h'],
#                 "percent_change_7d": crypto['quote']['USD']['percent_change_7d'],
#                 "percent_change_30d": crypto['quote']['USD']['percent_change_30d'],
#                 "percent_change_60d": crypto['quote']['USD']['percent_change_60d'],
#                 "percent_change_90d": crypto['quote']['USD']['percent_change_90d'],
#
#             }
#             for crypto in data['data']
#         ]
#         for crypto in cryptocurrencies:
#             StockData.objects.create(
#                 name=crypto['name'],
#                 symbol=crypto['symbol'],
#                 price=Decimal(crypto['price'].replace('$', '').replace(',', '')),
#                 market_cap=Decimal(crypto['market_cap'].replace('$', '').replace(',', '')),
#                 change_percentage=Decimal(crypto['change_percentage']),
#                 volume_24h=Decimal(crypto['volume_24h']),
#                 volume_change_24h=Decimal(crypto['volume_change_24h']),
#                 lasthour=Decimal(crypto['percent_change_1h']),
#                 last24h=Decimal(crypto['percent_change_24h']),
#                 week=Decimal(crypto['percent_change_7d']),
#                 month=Decimal(crypto['percent_change_30d']),
#                 TwoMonths=Decimal(crypto['percent_change_60d']),
#                 ThreeMonths=Decimal(crypto['percent_change_90d']),
#             )
#         print(cryptocurrencies)
#
#     else:
#         # If the API request fails, provide some default data or handle the error as needed
#         cryptocurrencies = [
#             {"name": "Bitcoin", "symbol": "BTC", "price": "$60,000", "market_cap": "$1.2 Trillion",
#              "change_percentage": "+5"},
#             # Add more default cryptocurrencies as needed
#         ]
#     print(cryptocurrencies)
#     return render(request, 'CryptoWebsite/home.html', {'cryptocurrencies': cryptocurrencies})

def stocks(request):
    # CoinMarketCap API endpoint for cryptocurrency listings
    api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    # Add your CoinMarketCap API key here
    api_key = '3ebb690c-aa21-4b14-bcd7-c84b1b48420e'

    # Define parameters for the API request
    params = {
        'start': '1',
        'limit': '20',
        'convert': 'USD'
    }

    # Set headers, including the API key
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    # Make the API request
    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract relevant information from the response
        cryptocurrencies = [
            {
                'name': crypto['name'],
                'symbol': crypto['symbol'],
                'price': '${:,.2f}'.format(crypto['quote']['USD']['price']),
                'market_cap': '${:,.2f}'.format(crypto['quote']['USD']['market_cap']),
                'change_percentage': '{:.2f}'.format(crypto['quote']['USD']['percent_change_24h']),
                'volume_24h': crypto['quote']['USD']['volume_24h'],
                "volume_change_24h": crypto['quote']['USD']['volume_change_24h'],
                "percent_change_1h": crypto['quote']['USD']['percent_change_1h'],
                "percent_change_24h": crypto['quote']['USD']['percent_change_24h'],
                "percent_change_7d": crypto['quote']['USD']['percent_change_7d'],
                "percent_change_30d": crypto['quote']['USD']['percent_change_30d'],
                "percent_change_60d": crypto['quote']['USD']['percent_change_60d'],
                "percent_change_90d": crypto['quote']['USD']['percent_change_90d'],
            }
            for crypto in data['data']
        ]
    else:
        # If the API request fails, provide some default data or handle the error as needed
        cryptocurrencies = [
            {"name": "Bitcoin", "symbol": "BTC", "price": "$60,000", "market_cap": "$1.2 Trillion",
             "change_percentage": "+5"},
            # Add more default cryptocurrencies as needed
        ]
    for crypto in cryptocurrencies:
        StockData.objects.create(
    name = crypto['name'],
    symbol = crypto['symbol'],
    price = Decimal(crypto['price'].replace('$', '').replace(',', '')),
    market_cap = Decimal(crypto['market_cap'].replace('$', '').replace(',', '')),
    change_percentage = Decimal(crypto['change_percentage']),
    volume_24h = Decimal(crypto['volume_24h']),
    volume_change_24h = Decimal(crypto['volume_change_24h']),
    lasthour = Decimal(crypto['percent_change_1h']),
    last24h = Decimal(crypto['percent_change_24h']),
    week = Decimal(crypto['percent_change_7d']),
    month = Decimal(crypto['percent_change_30d']),
    TwoMonths = Decimal(crypto['percent_change_60d']),
    ThreeMonths = Decimal(crypto['percent_change_90d']),

)
    return render(request, 'CryptoWebsite/stocks.html', {'cryptocurrencies': cryptocurrencies})

def make_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Process the payment and save payment details
            user = request.user
            amount = form.cleaned_data['amount']
            currency = form.cleaned_data['currency']
            card_number = form.cleaned_data['card_number']
            expiration_date = form.cleaned_data['expiration_date']
            cvv = form.cleaned_data['cvv']

            # Perform payment processing logic here (e.g., using a payment gateway API)

            # Save payment details in the database
            payment = Payment.objects.create(
                user=user,
                amount=amount,
                currency=currency,
                transaction_id='123456',  # Replace with actual transaction ID from payment gateway
            )

            return render(request, 'CryptoWebsite/payment_success.html', {'payment': payment})
    else:
        form = PaymentForm()

    return render(request, 'CryptoWebsite/make_payment.html', {'form': form})


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'CryptoWebsite/thank_you.html')  # Create a thank you page
    else:
        form = FeedbackForm()

    return render(request, 'CryptoWebsite/feedback_form.html', {'form': form})