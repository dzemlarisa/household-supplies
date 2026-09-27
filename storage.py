import json
import os

from models import Category, Operation, Stock, User
from models.operations import Operation as Op


def _load_raw(filename: str) -> list[dict]:
    """Прочитать список словарей из JSON-файла."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                print(f"Предупреждение: {filename} не список.")
                return []
            return data
    except json.JSONDecodeError:
        print(
            f"Предупреждение: файл {filename} повреждён, "
            f"используется пустой список."
        )
        return []
    except OSError as error:
        print(f"Ошибка чтения {filename}: {error}")
        return []


def _save_raw(filename: str, data: list[dict]) -> None:
    """Записать список словарей в JSON-файл."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Ошибка записи {filename}: {error}")


def load_categories(filename: str) -> list[Category]:
    """Загрузить категории."""
    return [Category.from_data(d) for d in _load_raw(filename)]


def save_categories(filename: str, categories: list[Category]) -> None:
    """Сохранить категории."""
    _save_raw(filename, [c.to_data() for c in categories])


def load_users(filename: str) -> list[User]:
    """Загрузить пользователей."""
    return [User.from_data(d) for d in _load_raw(filename)]


def save_users(filename: str, users: list[User]) -> None:
    """Сохранить пользователей."""
    _save_raw(filename, [u.to_data() for u in users])


def load_stocks(
    filename: str,
    categories: list[Category],
) -> list[Stock]:
    """Загрузить запасы, связав их с категориями."""
    result: list[Stock] = []
    for d in _load_raw(filename):
        try:
            result.append(Stock.from_data(d, categories))
        except ValueError as error:
            print(f"Пропущена запись запаса: {error}")
    return result


def save_stocks(filename: str, stocks: list[Stock]) -> None:
    """Сохранить запасы."""
    _save_raw(filename, [s.to_data() for s in stocks])


def load_operations(
    filename: str,
    stocks: list[Stock],
) -> list[Operation]:
    """Загрузить операции, связав их с запасами."""
    result: list[Operation] = []
    for d in _load_raw(filename):
        try:
            result.append(Op.from_data(d, stocks))
        except ValueError as error:
            print(f"Пропущена запись операции: {error}")
    return result


def save_operations(filename: str, operations: list[Operation]) -> None:
    """Сохранить операции."""
    _save_raw(filename, [o.to_data() for o in operations])
