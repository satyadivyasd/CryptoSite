"""
URL configuration for IADSProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from CryptoWebsite import views
from CryptoWebsite.views import FetchStockDataView, CryptoDataView, stocks, crypto_volume_chart

urlpatterns = [
    # path('', admin.site.urls),  # Assuming 'home' is the name of your view function for the root path
    path('admin/', admin.site.urls),
    path("",views.home,name='home'),
    path('convert_currency/<int:amount>/<str:from_currency>/<str:to_currency>/', views.convert_currency, name='convert_currency'),
    # path('monthly_stock_data',views.monthly_stock_data,name='monthly_stock_data'),
    path('chart',views.chart,name='chart'),
    path('data',views.data,name='data'),
    # path('stocks',views.stocks,name='stocks'),
    # path('stocks/', stocks.as_view(), name='stocks'),
    path('graph/', crypto_volume_chart, name='crypto_volume_chart'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('myaccount/', views.myaccount, name='myaccount'),
    path('generate_graph',views.generate_graph,name='generate_graph'),
    path('fetch_stock_data/', FetchStockDataView.as_view(), name='fetch_stock_data'),
    # path('last-year-crypto-data/', LastYearCryptoDataView.as_view(), name='last_year_crypto_data'),

    path('crypto-data/', CryptoDataView.as_view(), name='crypto_data'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
