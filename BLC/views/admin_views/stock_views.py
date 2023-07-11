from django.shortcuts import render
from BLC.models import Stock

def show_stock_page(request):
    search_mode = request.GET.get('search_mode')
    print(search_mode)
    stock_list = Stock.objects.select_related('item').order_by('item_id')
    
    range = []
    # under 5
    if search_mode == 'A':
        range = [0, 5]
    # between 5~10
    elif search_mode == 'B':
        range = [6, 10]
    # between 10~20
    elif search_mode == 'C':
        range = [11, 20]
    else:
        range = [0, 100]

    stock_list = Stock.objects.select_related('item').filter(quantity__range=range).order_by('quantity', 'item_id')
    
    context = {
        'stocks': stock_list
    }
    return render(request, 'admin/stock.html', context)


