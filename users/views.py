import sqlite3
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

DB_PATH = "data/homestock.sqlite"

def users_list(request: HttpRequest) -> HttpResponse:
    """Страница /users/ (SELECT)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    users = conn.execute("SELECT id, name, email FROM users ORDER BY name;").fetchall()
    conn.close()
    return render(request, "users/user_list.html", {"users": users})


def user_detail(request: HttpRequest, user_id: int) -> HttpResponse:
    """Страница /users/<id>/ (SELECT + WHERE)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    user = conn.execute("SELECT id, name, email FROM users WHERE id = ?;", (user_id,)).fetchone()
    
    if user is None:
        conn.close()
        return render(request, "users/user_detail.html", {"user_obj": None}, status=404)

    user_stocks = conn.execute("""
        SELECT stocks.id, stocks.name, stocks.quantity, stocks.unit
        FROM stocks
        WHERE stocks.user_id = ?;
    """, (user_id,)).fetchall()
    
    conn.close()
    
    context = {"user_obj": user, "user_stocks": user_stocks}
    return render(request, "users/user_detail.html", context)


def statistics(request: HttpRequest) -> HttpResponse:
    """Страница со статистикой по категориям (GROUP BY)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    stats = conn.execute("""
        SELECT categories.name AS category_name, COUNT(stocks.id) AS stock_count
        FROM categories
        LEFT JOIN stocks ON categories.id = stocks.category_id
        GROUP BY categories.name
        ORDER BY stock_count DESC;
    """).fetchall()
    conn.close()
    return render(request, "users/statistics.html", {"stats": stats})