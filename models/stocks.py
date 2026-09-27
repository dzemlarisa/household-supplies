from datetime import date

from .categories import Category, find_category_by_id


class Stock:
    """Домашний запас (товар)."""

    def __init__(
        self,
        stock_id: int,
        name: str,
        category: Category,
        quantity: float,
        unit: str,
        expiry_date: date | None = None,
    ) -> None:
        """Создать объект запаса."""
        self.id = stock_id
        self.name = name
        self.category = category
        self.quantity = round(quantity, 2)
        self.unit = unit
        self.expiry_date = expiry_date

    def __str__(self) -> str:
        """Строковое представление запаса."""
        return (
            f"Stock(id={self.id}, name='{self.name}', "
            f"category='{self.category.name}', "
            f"quantity={self.quantity} {self.unit})"
        )

    def change_quantity(self, delta: float) -> None:
        """Изменить количество запаса на delta.

        delta > 0 — приход, delta < 0 — расход.
        """
        new_quantity = round(self.quantity + delta, 2)
        if new_quantity < 0:
            raise ValueError("Количество не может быть отрицательным.")
        self.quantity = new_quantity

    @classmethod
    def from_data(
        cls,
        data: dict,
        categories: list[Category],
    ) -> "Stock":
        """Создать запас из данных JSON, связав его с категорией."""
        category = find_category_by_id(categories, data["category_id"])
        if category is None:
            raise ValueError(
                f"Категория id={data['category_id']} не найдена."
            )
        expiry = data.get("expiry_date")
        expiry_date = date.fromisoformat(expiry) if expiry else None
        return cls(
            stock_id=data["id"],
            name=data["name"],
            category=category,
            quantity=data["quantity"],
            unit=data["unit"],
            expiry_date=expiry_date,
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "category_id": self.category.id,
            "quantity": self.quantity,
            "unit": self.unit,
            "expiry_date": (
                self.expiry_date.isoformat() if self.expiry_date else None
            ),
        }


def add_stock(
    stocks: list[Stock],
    name: str,
    category: Category,
    quantity: float,
    unit: str,
    expiry_date: date | None = None,
) -> Stock:
    """Создать запас и добавить его в коллекцию."""
    new_id = max((s.id for s in stocks), default=0) + 1
    stock = Stock(new_id, name, category, quantity, unit, expiry_date)
    stocks.append(stock)
    return stock


def find_stock(stocks: list[Stock], query: str) -> list[Stock]:
    """Найти запасы по подстроке в названии."""
    q = query.lower()
    return [s for s in stocks if q in s.name.lower()]


def find_stock_by_id(stocks: list[Stock], stock_id: int) -> Stock | None:
    """Найти запас по идентификатору."""
    for s in stocks:
        if s.id == stock_id:
            return s
    return None


def filter_stocks_by_category(
    stocks: list[Stock],
    category: Category,
) -> list[Stock]:
    """Отобрать запасы по объекту категории."""
    return [s for s in stocks if s.category.id == category.id]


def sort_stocks_by_name(stocks: list[Stock]) -> list[Stock]:
    """Отсортировать запасы по названию."""
    return sorted(stocks, key=lambda s: s.name.lower())


def sort_stocks_by_quantity(stocks: list[Stock]) -> list[Stock]:
    """Отсортировать запасы по количеству."""
    return sorted(stocks, key=lambda s: s.quantity)


def delete_stock(stocks: list[Stock], stock_id: int) -> Stock:
    """Удалить запас из коллекции."""
    stock = find_stock_by_id(stocks, stock_id)
    if stock is None:
        raise ValueError(f"Запас id={stock_id} не найден.")
    stocks.remove(stock)
    return stock


def get_statistics(stocks: list[Stock]) -> dict:
    """Сводная статистика по запасам."""
    by_category: dict[str, int] = {}
    for s in stocks:
        key = s.category.name
        by_category[key] = by_category.get(key, 0) + 1
    return {
        "total": len(stocks),
        "by_category": by_category,
    }
