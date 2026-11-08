from django.shortcuts import render, get_object_or_404
from users.models import User
from stocks.models import Stock
from django.db.models import Count, Q

def users_list(request):
    users = User.objects.all()
    return render(request, "users/user_list.html", {"users": users})

def user_detail(request, user_id):
    user_obj = get_object_or_404(User, pk=user_id)
    user_stocks = user_obj.stocks.all()
    return render(request, "users/user_detail.html", {"user_obj": user_obj, "user_stocks": user_stocks})

def statistics(request):
    stats = User.objects.annotate(
        stock_count=Count("stocks")
    ).order_by("-stock_count")
    return render(request, "users/statistics.html", {"stats": stats})