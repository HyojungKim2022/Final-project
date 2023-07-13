from django.shortcuts import render
from django.http import JsonResponse

from BLC.models import Sales, DetailSale
from django.db import connection

# Create your views here.
def show_sales_page(request):
    return render(request, 'admin/sales.html')

# 일자별 판매액
def get_daily_sales(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT sale_date, total_amount
            FROM DAILY_SALES
        """)
        daily_sales = cursor.fetchall()
    response_data = {
        sale_date.strftime('%Y-%m-%d'):int(total_amount)
        for sale_date, total_amount in daily_sales
    }
    return JsonResponse(response_data, safe=False)

# 판매사항
def get_sales(request, salesKey):
    sales = Sales.objects.filter(sale_date=salesKey).order_by('sale_date').values('sale_id', 'sale_date', 'total_price')
    
    sales_list = list(sales)

    response_data = {
        'sales': sales_list
    }
    return JsonResponse(response_data)

# 세부 판매사항
def get_detail_sales(request, saleId):
    detail_sale = DetailSale.objects.select_related('item').filter(sale=saleId).order_by('item').values('item', 'item__item_name', 'quantity', 'unit_price')
    detail_sale = list(detail_sale)
    respon_data = {
        'detail_sales':detail_sale
    }
    return JsonResponse(respon_data)