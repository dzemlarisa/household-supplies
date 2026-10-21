import sqlite3
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render

DB_PATH = "data/homestock.sqlite"

def stocks_list(request: HttpRequest) -> HttpResponse:
    """Страница /stocks/ — список запасов (SQL SELECT)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    stocks = conn.execute("""
        SELECT stocks.id, stocks.name, stocks.quantity, stocks.unit, 
               categories.name AS category_name
        FROM stocks
        JOIN categories ON stocks.category_id = categories.id
        ORDER BY stocks.name;
    """).fetchall()
    conn.close()

    return render(request, "stocks/stock_list.html", {"stocks": stocks})


def stock_detail(request: HttpRequest, stock_id: int) -> HttpResponse:
    """Страница /stocks/<id>/ (SQL SELECT + JOIN)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    stock = conn.execute("""
        SELECT stocks.id, stocks.name, stocks.quantity, stocks.unit, stocks.expiry_date,
               categories.name AS category_name, users.name AS owner_name
        FROM stocks
        JOIN categories ON stocks.category_id = categories.id
        JOIN users ON stocks.user_id = users.id
        WHERE stocks.id = ?;
    """, (stock_id,)).fetchone()
    conn.close()

    if stock is None:
        raise Http404("Запас не найден")

    return render(request, "stocks/stock_detail.html", {"stock": stock})