from django.shortcuts import render
from BLC.models import Items, Store, Stock

def show_stock_page(request):
    stock = Stock.objects.select_related('item')
    context = {
        'stocks': stock
    }
    return render(request, 'admin/stock.html', context)


