import requests
from django.http import JsonResponse
from django.shortcuts import render


def CurrencyExchange(request):
    base_currency = request.GET.get('base', 'USD')  # Default base currency is USD
    target_currency = request.GET.get('target', 'EUR')  # Default target currency is EUR

    api_url = f'https://api.exchangeratesapi.io/latest?base={base_currency}&symbols={target_currency}'

    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Unable to fetch currency exchange rate'}, status=500)


# views.py
import requests
from django.http import JsonResponse

import requests
from django.http import JsonResponse


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
