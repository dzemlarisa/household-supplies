from django.http import HttpResponse, HttpRequest

from homepage.views import page
from models.operations import find_operation_by_id
from storage import (
    load_categories,
    load_operations,
    load_stocks,
    load_users,
)

CATEGORIES_FILE = "data/categories.json"
USERS_FILE = "data/users.json"
STOCKS_FILE = "data/stocks.json"
OPERATIONS_FILE = "data/operations.json"


def _load_all():
    """Загрузить весь набор данных проекта."""
    categories = load_categories(CATEGORIES_FILE)
    users = load_users(USERS_FILE)
    stocks = load_stocks(STOCKS_FILE, categories, users)
    operations = load_operations(OPERATIONS_FILE, stocks)
    return stocks, operations


def operations_list(request: HttpRequest) -> HttpResponse:
    """Страница /operations/ — список операций."""
    _, operations = _load_all()
    items = ""
    for o in operations:
        kind = "приход" if o.type == "restock" else "расход"
        badge = "bg-success" if o.type == "restock" else "bg-warning"
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between">'
            f'<a href="/operations/{o.id}/">'
            f'{o.stock.name} — {o.date.isoformat()}</a>'
            f'<span class="badge {badge}">{kind} '
            f'{o.amount}</span></li>'
        )
    if not items:
        items = '<li class="list-group-item">Операций пока нет.</li>'
    content = f"""
<h1>Операции</h1>
<ul class="list-group">{items}</ul>
"""
    return HttpResponse(page("HomeStock — операции", content))


def operation_detail(
    request: HttpRequest,
    operation_id: int,
) -> HttpResponse:
    """Страница /operations/<id>/ — карточка операции."""
    _, operations = _load_all()
    op = find_operation_by_id(operations, operation_id)
    if op is None:
        content = """
<h1 class="text-danger">Операция не найдена</h1>
<a href="/operations/" class="btn btn-outline-secondary">
  ← к списку операций
</a>
"""
        return HttpResponse(
            page("Операция не найдена", content),
            status=404,
        )

    kind = "приход" if op.type == "restock" else "расход"
    badge = "bg-success" if op.type == "restock" else "bg-warning"
    content = f"""
<div class="card">
  <div class="card-body">
    <h5 class="card-title">Операция №{op.id}</h5>
    <p class="card-text"><strong>Запас:</strong>
      <a href="/stocks/{op.stock.id}/">{op.stock.name}</a></p>
    <p class="card-text"><strong>Тип:</strong>
      <span class="badge {badge}">{kind}</span></p>
    <p class="card-text"><strong>Количество:</strong>
      {op.amount} {op.stock.unit}</p>
    <p class="card-text"><strong>Дата:</strong>
      {op.date.isoformat()}</p>
    <a href="/operations/" class="btn btn-outline-secondary">
      ← к списку операций
    </a>
  </div>
</div>
"""
    return HttpResponse(page(f"Операция №{op.id}", content))
