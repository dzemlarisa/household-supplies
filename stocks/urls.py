from django.urls import path
from . import views

app_name = "stocks"

urlpatterns = [
    path("", views.stocks_list, name="list"),
    path("<int:stock_id>/", views.stock_detail, name="detail"),
]