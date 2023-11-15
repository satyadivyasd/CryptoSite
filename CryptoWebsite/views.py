from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.shortcuts import render, get_object_or_404
import requests
from django.http import JsonResponse
import plotly.express as px
import calendar
from .forms import DateForm
from .models import StockData, PaymentHistory

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
    result = {
        'converted_amount': converted_amount
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

def paymentHistory(request):
    paymentHistory = get_object_or_404(PaymentHistory)
    return render(request, 'paymentHistory.html', {'paymentHistoryDetails' : paymentHistory})