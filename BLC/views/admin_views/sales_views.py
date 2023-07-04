from django.shortcuts import render
from BLC.models import Sales, DetailSale, Daily_Sales

# Create your views here.
def show_sales_page(request):
    return render(request, 'admin/sales.html')


# 값 받아 넣기
def get_daily_sales(request, salesKey):
    d_sales = Daily_Sales.objects.get(salesKey)
    # SalesData 넣기

# 
def get_sales_details(request, salesKey):


    return 0