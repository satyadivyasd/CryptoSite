from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.shortcuts import render
import requests
from django.http import JsonResponse
import plotly.express as px
import calendar
from .forms import DateForm
from .models import StockData,Currency

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
        return render(request, 'tradeinfo.html', result)


    else:
        return JsonResponse({'success': False, 'error': 'Failed to retrieve data from the API'})

def monthly_stock_data(request):
    # Get monthly aggregated stock data
    stock_data_list = StockData.objects.all().order_by('date').asc
    # Process stock_data_list to get data for the chart
    context = {
        'stock_data_list': stock_data_list,
    }
    return render(request, 'monthly_stock_data.html', context)

def home(request):
    return render(request,'home.html')
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
    return render(request, 'chart.html', context)


# views.py
from django.shortcuts import render
import requests

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

            return render(request, 'crypto_data.html', context)

        else:
            # If the request was not successful, handle the error
            return render(request, 'error.html', {'error_message': 'Failed to retrieve crypto data'})

    except requests.RequestException as e:
        # Handle any exceptions that might occur during the request
        return render(request, 'error.html', {'error_message': f'Request error: {str(e)}'})
