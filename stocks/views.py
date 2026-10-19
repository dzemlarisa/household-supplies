from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.stocks import find_stock_by_id
from storage import load_categories, load_stocks, load_users

CATEGORIES_FILE = "data/categories.json"
USERS_FILE = "data/users.json"
STOCKS_FILE = "data/stocks.json"

def stocks_list(request: HttpRequest) -> HttpResponse:
    """Страница /stocks/ — список запасов."""
    categories = load_categories(CATEGORIES_FILE)
    users = load_users(USERS_FILE)
    stocks = load_stocks(STOCKS_FILE, categories, users)
    
    context = {"stocks": stocks}
    return render(request, "stocks/stock_list.html", context)

def stock_detail(request: HttpRequest, stock_id: int) -> HttpResponse:
    """Страница /stocks/<id>/ — карточка запаса."""
    categories = load_categories(CATEGORIES_FILE)
    users = load_users(USERS_FILE)
    stocks = load_stocks(STOCKS_FILE, categories, users)
    
    stock = find_stock_by_id(stocks, stock_id)
    
    context = {"stock": stock}
    return render(
        request, 
        "stocks/stock_detail.html", 
        context,
        status=404 if stock is None else 200
    )