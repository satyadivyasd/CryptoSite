from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.shortcuts import render, get_object_or_404, redirect
import requests
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
import plotly.express as px
import calendar
from django.shortcuts import render
from django.views import View
import requests
import requests
from django.shortcuts import render
import matplotlib.pyplot as plt
from io import BytesIO
import base64



from django.urls import reverse

from .forms import DateForm
from .models import StockData,Currency
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, UserProfileForm
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
    c=Currency.objects.all()
    result = {
        'converted_amount': converted_amount,
        'currencies':c,
    }
    if response.status_code == 200:
        return render(request, 'CryptoWebsite/tradeinfo.html', result)


    else:
        return JsonResponse({'success': False, 'error': 'Failed to retrieve data from the API'})

def monthly_stock_data(request):
    # Get monthly aggregated stock data
    stock_data_list = StockData.objects.all().order_by('date').asc
    # Process stock_data_list to get data for the chart
    context = {
        'stock_data_list': stock_data_list,
    }
    return render(request, 'CryptoWebsite/monthly_stock_data.html', context)

def home(request):
    return render(request, 'CryptoWebsite/home.html')
# Create your views here.
def chart(request):
    # start = request.GET.get('start')
    # end = request.GET.get('end')

    co2 = StockData.objects.all().order_by('date')
    # if start:
    #     co2 = co2.filter(date__gte=start)
    # if end:
    #     co2 = co2.filter(date__lte=end)

    fig = px.line(
        x=[c.date for c in co2],
        y=[c.stock_rate for c in co2],
        # title="CO2 PPM",
        # labels={'x': 'Date', 'y': 'CO2 PPM'}
    )

    fig.update_layout(
        title={
            'font_size': 24,
            'xanchor': 'center',
            'x': 0.5
    })
    chart = fig.to_html()
    context = {'chart': chart, 'form': DateForm()}
    return render(request, 'CryptoWebsite/chart.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')

def crypto_data(request):
    # Replace 'bitcoin' with the desired cryptocurrency symbol or ID
    crypto_symbol = 'bitcoin'

    # CoinGecko API endpoint for cryptocurrency data
    api_url = f'https://api.coingecko.com/api/v3/coins/{crypto_symbol}'

    try:
        # Make a GET request to the CoinGecko API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data from the response
            crypto_info = response.json()

            # Extract relevant data from the JSON response
            crypto_name = crypto_info['name']
            crypto_price = crypto_info['market_data']['current_price']['usd']
            crypto_market_cap = crypto_info['market_data']['market_cap']['usd']

            # You can pass this data to the template or use it as needed
            context = {
                'crypto_name': crypto_name,
                'crypto_price': crypto_price,
                'crypto_market_cap': crypto_market_cap,
            }

            return render(request, 'CryptoWebsite/crypto_data.html', context)

        else:
            # If the request was not successful, handle the error
            return render(request, 'CryptoWebsite/error.html', {'error_message': 'Failed to retrieve crypto data'})

    except requests.RequestException as e:
        # Handle any exceptions that might occur during the request
        return render(request, 'CryptoWebsite/error.html', {'error_message': f'Request error: {str(e)}'})


# def paymentHistory(request):
#     paymentHistory = get_object_or_404(PaymentHistory)
#     print("paymentHistory list is fetched.")
#     return render(request, 'paymentHistory.html', {'paymentHistoryDetails' : paymentHistory})

# views.py in your app
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
            return render(request, 'CryptoWebsite/register.html', {'user_form': user_form, 'profile_form': profile_form, 'user_errors': user_errors, 'profile_errors': profile_errors})

    else:
        user_form = RegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'CryptoWebsite/register.html', {'user_form': user_form, 'profile_form': profile_form})

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
    # Get the current user's profile
    user_profile = request.user.userprofile

    return render(request, 'CryptoWebsite/userprofile.html', {'user_profile': user_profile})


class stocks(View):
    def get(self, request, *args, **kwargs):
        api_key = "3ebb690c-aa21-4b14-bcd7-c84b1b48420e"
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': api_key,
        }

        # Calculate the date one year ago from today
        last_year_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

        params = {
            'start_date': last_year_date,
            'limit': 500,  # Adjust the limit as needed
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json().get('data', [])

        for crypto in data:
            name = crypto.get('name')
            symbol = crypto.get('symbol')
            price = crypto.get('quote', {}).get('USD', {}).get('price')
            timestamp=crypto.get('timestamp')
            data=StockData(name=name,symbol=symbol,price=price,timestamp=timestamp)
            data.save()
            print(f"Name: {name}, Symbol: {symbol}, Price: {price}")


        return HttpResponse("Check console for data")




def generate_graph(request):
    api_url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/price-performance-stats/latest"
    api_key = "3ebb690c-aa21-4b14-bcd7-c84b1b48420e"  # Replace with your actual API key

    headers = {
        "X-CMC_PRO_API_KEY": api_key,
    }

    try:
        response = requests.get(api_url, headers=headers)
        data = response.json()

        # Extract relevant data for plotting (example: prices)
        timestamps = data["data"]["timestamps"]
        prices = data["data"]["prices"]

        # Create a simple line plot
        plt.plot(timestamps, prices)
        plt.xlabel("Timestamp")
        plt.ylabel("Price")
        plt.title("Cryptocurrency Price Performance")

        # Save the plot to a BytesIO buffer
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close()

        # Convert the plot to base64 for embedding in HTML
        plot_data = base64.b64encode(buffer.read()).decode("utf-8")

        # Pass the plot_data to the template
        context = {"plot_data": plot_data}
        return render(request, "CryptoWebsite/generate_graph.html", context)

    except Exception as e:
        return render(request, "CryptoWebsite/home.html", {"error_message": str(e)})

# views.py



class FetchStockDataView(View):
    def get(self, request, *args, **kwargs):
        api_key = "3ebb690c-aa21-4b14-bcd7-c84b1b48420e"  # Replace with your actual CoinMarketCap API key
        symbols = ['BTC', 'ETH', 'XRP']  # Replace with the symbols of the stocks you're interested in

        for symbol in symbols:
            historical_data = self.fetch_historical_data(api_key, symbol)
            self.save_to_model(symbol, historical_data)

        return JsonResponse({'message': 'Stock data fetched and stored successfully'})

    def fetch_historical_data(self, api_key, symbol):
        url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/price-performance-stats/historical"
        parameters = {
            'symbol': symbol,
            'time_period': '730d',  # 730 days for the last two years
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': api_key,
        }

        try:
            response = requests.get(url, params=parameters, headers=headers)
            data = response.json()
            return data.get('data', {}).get('quotes', [])

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return []

    def save_to_model(self, symbol, historical_data):
        for entry in historical_data:
            timestamp = datetime.utcfromtimestamp(entry['timestamp'] / 1000.0)
            stock_data, created = StockData.objects.get_or_create(
                symbol='all',
                timestamp=timestamp,
                defaults={'price': entry['quote']['USD']['price']}
                # Add other fields as needed
            )
            if not created:
                # Update existing record if needed
                stock_data.price = entry['quote']['USD']['price']
                stock_data.save()

# views.py

class CryptoDataView(View):
    def get(self, request, *args, **kwargs):
        api_key = '3ebb690c-aa21-4b14-bcd7-c84b1b48420e'
        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/ohlcv/historical'

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': api_key,
        }

        params = {
            'symbol': 'BTC',  # Replace with the symbol of the cryptocurrency you are interested in
            'time_period': 'daily',
            'count': 10,  # Number of data points to retrieve
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json().get('data', {}).get('quotes', [])

        for quote in data:
            timestamp = quote.get('time_open')
            open_price = quote.get('open')
            high_price = quote.get('high')
            low_price = quote.get('low')
            close_price = quote.get('close')
            volume = quote.get('volume')

            print(f"Timestamp: {timestamp}, Open: {open_price}, High: {high_price}, Low: {low_price}, Close: {close_price}, Volume: {volume}")

        return HttpResponse("Check console for data")

def stockdata(request):
    # def get(self, request, *args, **kwargs):
    #     api_key = 'YOUR_COINMARKETCAP_API_KEY'
    #     url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    #
    #     headers = {
    #         'Accepts': 'application/json',
    #         'X-CMC_PRO_API_KEY': api_key,
    #     }
    #
    #     last_year_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    #
    #     params = {
    #         'start_date': last_year_date,
    #         'limit': 100,  # Adjust the limit as needed
    #     }
    #
    #     response = requests.get(url, headers=headers, params=params)
    #     data = response.json().get('data', [])
    #
    #     for crypto in data:
    #         name = crypto.get('name')
    #         symbol = crypto.get('symbol')
    #         price = crypto.get('quote', {}).get('USD', {}).get('price')
    #         timestamp=crypto.get('timestamp')
    #         # Save data in the CryptoCurrency model
    #         print (name,price)
    #         data=StockData(name=name, symbol=symbol, price=price,timestamp=timestamp)
    #         data.save()
    #     return HttpResponse("Crypto data from the last year saved in the model")
        # CoinMarketCap API endpoint for cryptocurrency listings
        api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        # Add your CoinMarketCap API key here
        api_key = '3ebb690c-aa21-4b14-bcd7-c84b1b48420e'
        # Define parameters for the API request
        params = {
            'start': '1',
            'limit': '10',
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
                    'volume':crypto['volume_30d']
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
            return HttpResponse(cryptocurrencies)
        # return render(request, 'home.html', {'cryptocurrencies': cryptocurrencies})



def data(request):
    # CoinMarketCap API endpoint for cryptocurrency listings
    api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    # Add your CoinMarketCap API key here
    api_key = '3ebb690c-aa21-4b14-bcd7-c84b1b48420e'
    # Define parameters for the API request
    params = {
        'start': '1',
        'limit': '10',
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
                'volume':crypto['quote']['USD'].get('volume_30d',0)
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
    print (cryptocurrencies)
    return render(request, 'CryptoWebsite/home.html', {'cryptocurrencies': cryptocurrencies})

#     # CoinMarketCap API endpoint for cryptocurrency historical data
#     api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/historical'
#
#     # Add your CoinMarketCap API key here
#     api_key = '3ebb690c-aa21-4b14-bcd7-c84b1b48420e'
#
#     # Define parameters for the API request
#     params = {
#         'symbol': 'BTC',  # Set to 'BTC' for Bitcoin
#         'interval': 'daily',
#         'time_start': (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
#         'time_end': datetime.now().strftime('%Y-%m-%d'),
#         'convert': 'USD'
#     }
#
#     # Set headers, including the API key
#     headers = {
#         'Accepts': 'application/json',
#         'X-CMC_PRO_API_KEY': api_key,
#     }
#
#     # Make the API request
#     response = requests.get(api_url, headers=headers, params=params)
#
#     if response.status_code == 200:
#         # Parse the JSON response
#         data = response.json()
#         print ("success")
#         # Extract relevant information from the response
#         cryptocurrencies = [
#             {
#                 'timestamp': crypto['timestamp'],
#                 'price': '${:,.2f}'.format(crypto['quote']['USD']['close']),
#                 'market_cap': '${:,.2f}'.format(crypto['quote']['USD']['market_cap']),
#                 'volume': '${:,.2f}'.format(crypto['quote']['USD']['volume']),
#                 'change_percentage': '{:.2f}'.format(crypto['quote']['USD']['percent_change']),
#             }
#             for crypto in data['data']['quotes']
#         ]
#     else:
#         # If the API request fails, provide some default data or handle the error as needed
#         cryptocurrencies = [
#             {"timestamp": "2022-01-01", "price": "$60,000", "market_cap": "$1.2 Trillion",
#              "volume": "$100 billion", "change_percentage": "+5"},
#             # Add more default cryptocurrencies as needed
#         ]
#
#     print(cryptocurrencies)

#     return render(request, 'CryptoWebsite/home.html', {'cryptocurrencies': cryptocurrencies})

# def data(request):
#     # CoinMarketCap API endpoint for cryptocurrency historical data
#     api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/historical/'
#
#     # Add your CoinMarketCap API key here
#     api_key = '3ebb690c-aa21-4b14-bcd7-c84b1b48420e'
#
#     # Define parameters for the API request
#     params = {
#         'symbol': 'BTC',  # Set to 'BTC' for Bitcoin
#         'interval': 'daily',
#         'time_start': (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
#         'time_end': datetime.now().strftime('%Y-%m-%d'),
#         'convert': 'USD'
#     }
#
#     # Set headers, including the API key
#     headers = {
#         'Accepts': 'application/json',
#         'X-CMC_PRO_API_KEY': api_key,
#     }
#
#     # Make the API request
#     response = requests.get(api_url, headers=headers, params=params)
#     if response.status_code == 200:
#         # Parse the JSON response
#         data = response.json()
#         print(data)
#         # Extract relevant information from the response
#         cryptocurrencies = [
#             {
#                 'timestamp': crypto['timestamp'],
#                 'price': '${:,.2f}'.format(crypto['quote']['USD']['close']),
#                 'market_cap': '${:,.2f}'.format(crypto['quote']['USD']['market_cap']),
#                 'volume': '${:,.2f}'.format(crypto['quote']['USD']['volume']),
#                 'change_percentage': '{:.2f}'.format(crypto['quote']['USD']['percent_change']),
#             }
#             for crypto in data['data']['quotes']
#         ]
#     else:
#         # If the API request fails, provide some default data or handle the error as needed
#         cryptocurrencies = [
#             {"timestamp": "2022-01-01", "price": "$60,000", "market_cap": "$1.2 Trillion",
#              "volume": "$100 billion", "change_percentage": "+5"},
#             # Add more default cryptocurrencies as needed
#         ]
#
#     return render(request, 'CryptoWebsite/home.html', {'cryptocurrencies': cryptocurrencies})
# # # from django.shortcuts import render
# # import requests
# # from datetime import datetime, timedelta
# #
# # def data(request):
# #     # CoinAPI endpoint for cryptocurrency historical data
# #     api_url = 'https://rest.coinapi.io/v1/ohlcv/BTC/history'
# #
# #     # Add your CoinAPI key here
# #     api_key = 'CDB65F9C-6DED-4C25-9896-ACE3C0CF11D7'
# #
# #     # Define the symbols you are interested in
# #     symbols = ['BTC', 'ETH', 'XRP', 'LTC']  # Add more symbols as needed
# #
# #     # Define parameters for the API request
# #     params = {
# #         'period_id': '1DAY',
# #         'time_start': (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%S'),
# #         'limit': 365,  # Number of data points for the last year
# #     }
# #
# #     # Set headers, including the API key
# #     headers = {
# #         'X-CoinAPI-Key': api_key,
# #     }
# #
# #     # Initialize an empty list to store data for all cryptocurrencies
# #     cryptocurrencies_data = []
# #
# #     # Make API requests for each symbol
# #     for symbol in symbols:
# #         response = requests.get(api_url.format(symbol), headers=headers, params=params)
# #
# #         if response.status_code == 200:
# #             # Parse the JSON response
# #             data = response.json()
# #
# #             # Extract relevant information from the response
# #             cryptocurrency_data = {
# #                 'symbol': symbol,
# #                 'historical_data': [
# #                     {
# #                         'timestamp': entry['time_period_start'],
# #                         'price_open': entry['price_open'],
# #                         'price_high': entry['price_high'],
# #                         'price_low': entry['price_low'],
# #                         'price_close': entry['price_close'],
# #                         'volume_traded': entry['volume_traded'],
# #                     }
# #                     for entry in data
# #                 ],
# #             }
# #
# #             cryptocurrencies_data.append(cryptocurrency_data)
# #     print(cryptocurrencies_data,api_url)
# #     return render(request, 'CryptoWebsite/home.html', {'cryptocurrencies_data': cryptocurrencies_data})
# views.py



def crypto_volume_chart(request):
    # Replace 'YOUR_API_KEY' with your CoinMarketCap API key
    api_key = '3ebb690c-aa21-4b14-bcd7-c84b1b48420e'

    # CoinMarketCap API endpoint for historical data
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/historical'

    # Parameters for the API request
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }

    # Headers for the API request
    headers = {
        'X-CMC_PRO_API_KEY': api_key,
    }

    try:
        # Make the API request
        response = requests.get(url, params=parameters, headers=headers)
        data = response.json()

        # Check if 'data' key exists in the response
        if 'data' not in data:
            raise KeyError('Key "data" not found in API response')

        # Extract data for the chart (e.g., names and volumes)
        crypto_names = [crypto['name'] for crypto in data['data']]
        crypto_volumes = [crypto['quote']['USD']['volume'] for crypto in data['data']]

        # Pass data to the template
        context = {
            'crypto_names': crypto_names,
            'crypto_volumes': crypto_volumes,
        }

        return render(request, 'CryptoWebsite/generate_graph.html', context)

    except requests.exceptions.RequestException as e:
        # Handle errors
        return render(request, 'CryptoWebsite/home.html', {'error_message': str(e)})
    except KeyError as e:
        # Handle missing key error
        return render(request, 'CryptoWebsite/home.html', {'error_message': str(e)})
