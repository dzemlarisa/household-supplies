from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.users import find_user_by_id
from models.stocks import find_stock_by_owner
from storage import load_categories, load_stocks, load_users

CATEGORIES_FILE = "data/categories.json"
USERS_FILE = "data/users.json"
STOCKS_FILE = "data/stocks.json"


def users_list(request: HttpRequest) -> HttpResponse:
    """Страница со списком всех владельцев."""
    users = load_users(USERS_FILE)
    context = {"users": users}
    return render(request, "users/user_list.html", context)


def user_detail(request: HttpRequest, user_id: int) -> HttpResponse:
    """Страница конкретного владельца и его запасов."""
    categories = load_categories(CATEGORIES_FILE)
    users = load_users(USERS_FILE)
    stocks = load_stocks(STOCKS_FILE, categories, users)
    
    user_obj = find_user_by_id(users, user_id)
    
    user_stocks = []
    if user_obj is not None:
        user_stocks = find_stock_by_owner(stocks, user_obj)

    context = {
        "user_obj": user_obj,
        "user_stocks": user_stocks,
    }
    
    return render(
        request,
        "users/user_detail.html",
        context,
        status=404 if user_obj is None else 200,
    )