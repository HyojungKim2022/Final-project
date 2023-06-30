from django.shortcuts import render
from BLC.models import Items, Store, Stock

def post_view(request):
    items = Items.objects.all()
    stores = Store.objects.all()
    stocks = Stock.objects.all()
    return render(request, 'BLC/test.html', {'items' : items, 'stores':stores, 'stocks':stocks})

