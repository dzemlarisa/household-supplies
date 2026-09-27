"""Функции работы с домашними запасами."""
from datetime import date


def add_stock(
    stocks: list[dict],
    name: str,
    category: str,
    quantity: float,
    unit: str,
    expiry_date: date | None = None
) -> dict:
    """Добавить новый запас в список stocks и вернуть его."""
    new_id = max((s["id"] for s in stocks), default=0) + 1
    stock = {
        "id": new_id,
        "name": name,
        "category": category,
        "quantity": round(quantity, 2),
        "unit": unit,
        "expiry_date": expiry_date.isoformat() if expiry_date else None,
    }
    stocks.append(stock)
    return stock


def find_stock(stocks: list[dict], query: str) -> list[dict]:
    """Найти запасы по подстроке в названии."""
    query_lower = query.lower()
    return [s for s in stocks if query_lower in s["name"].lower()]


def find_stock_by_id(stocks: list[dict], stock_id: int) -> dict | None:
    """Найти запас по идентификатору."""
    for s in stocks:
        if s["id"] == stock_id:
            return s
    return None


def filter_stocks_by_category(
    stocks: list[dict], category: str
) -> list[dict]:
    """Отобрать запасы по категории."""
    category_lower = category.lower()
    return [
        s for s in stocks
        if s["category"].lower() == category_lower
    ]


def sort_stocks_by_quantity(stocks: list[dict]) -> list[dict]:
    """Отсортировать запасы по количеству (по возрастанию)."""
    return sorted(stocks, key=lambda s: s["quantity"])


def sort_stocks_by_name(stocks: list[dict]) -> list[dict]:
    """Отсортировать запасы по названию."""
    return sorted(stocks, key=lambda s: s["name"].lower())


def get_statistics(stocks: list[dict]) -> dict:
    """Вернуть статистику по запасам."""
    total = len(stocks)
    by_category: dict[str, int] = {}
    for s in stocks:
        by_category[s["category"]] = by_category.get(s["category"], 0) + 1
    return {
        "total": total,
        "by_category": by_category,
    }


def delete_stock(
    stocks: list[dict],
    stock_id: int
) -> dict:
    stock = find_stock_by_id(stocks, stock_id)
    if stock is None:
        raise ValueError(f"Запас с id={stock_id} не найден.")
    stocks.remove(stock)
    return stock
