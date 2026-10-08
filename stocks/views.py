from django.http import HttpResponse, HttpRequest

from homepage.views import page
from models.stocks import find_stock_by_id
from models.users import find_user_by_id
from storage import load_categories, load_stocks, load_users

CATEGORIES_FILE = "data/categories.json"
USERS_FILE = "data/users.json"
STOCKS_FILE = "data/stocks.json"


def _load_all():
    """Загрузить категории, пользователей и запасы."""
    categories = load_categories(CATEGORIES_FILE)
    users = load_users(USERS_FILE)
    stocks = load_stocks(STOCKS_FILE, categories, users)
    return categories, users, stocks


def stocks_list(request: HttpRequest) -> HttpResponse:
    """Страница /stocks/ — список запасов."""
    _, _, stocks = _load_all()
    items = ""
    for s in stocks:
        qty = f"{s.quantity} {s.unit}"
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between">'
            f'<a href="/stocks/{s.id}/">{s.name}</a>'
            f'<span class="text-muted">'
            f'{s.category.name} · {qty}</span>'
            f'</li>'
        )
    if not items:
        items = '<li class="list-group-item">Запасов пока нет.</li>'
    content = f"""
<h1>Запасы</h1>
<ul class="list-group">{items}</ul>
"""
    return HttpResponse(page("HomeStock — запасы", content))


def stock_detail(request: HttpRequest, stock_id: int) -> HttpResponse:
    """Страница /stocks/<id>/ — карточка запаса."""
    _, users, stocks = _load_all()
    stock = find_stock_by_id(stocks, stock_id)
    if stock is None:
        content = """
<h1 class="text-danger">Запас не найден</h1>
<a href="/stocks/" class="btn btn-outline-secondary">
  ← к списку запасов
</a>
"""
        return HttpResponse(
            page("Запас не найден", content),
            status=404,
        )

    owner = find_user_by_id(users, stock.owner.id)
    owner_name = owner.name if owner else "—"
    expiry = stock.expiry_date.isoformat() if stock.expiry_date else "—"
    content = f"""
<div class="card">
  <div class="card-body">
    <h5 class="card-title">{stock.name}</h5>
    <p class="card-text"><strong>ID:</strong> {stock.id}</p>
    <p class="card-text"><strong>Категория:</strong>
      {stock.category.name}</p>
    <p class="card-text"><strong>Владелец:</strong>
      {owner_name}</p>
    <p class="card-text"><strong>Количество:</strong>
      {stock.quantity} {stock.unit}</p>
    <p class="card-text"><strong>Срок годности:</strong>
      {expiry}</p>
    <a href="/stocks/" class="btn btn-outline-secondary">
      ← к списку запасов
    </a>
  </div>
</div>
"""
    return HttpResponse(page(stock.name, content))
