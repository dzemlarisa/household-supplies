from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from stocks.models import Stock

def stocks_list(request):
    stocks_list = Stock.objects.select_related("category", "owner").all()

    paginator = Paginator(stocks_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "stocks/stock_list.html", {"stocks": page_obj, "page_obj": page_obj})

def stock_detail(request, stock_id):
    stock = get_object_or_404(Stock.objects.select_related("category", "owner"), pk=stock_id)
    return render(request, "stocks/stock_detail.html", {"stock": stock})