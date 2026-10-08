from django.urls import path

from . import views

urlpatterns = [
    path("", views.stocks_list, name="stocks_list"),
    path("<int:stock_id>/", views.stock_detail, name="stock_detail"),
]
