"""Загрузка и сохранение данных HomeStock в JSON-файлах."""
import json
import os


def load_json(filename: str) -> list[dict]:
    """Загрузить список записей из JSON-файла.

    Возвращает пустой список, если файл отсутствует
    или содержит некорректный JSON.
    """
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                print(f"Предупреждение: {filename} не содержит список.")
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


def save_json(filename: str, data: list[dict]) -> None:
    """Сохранить список записей в JSON-файл."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Ошибка записи {filename}: {error}")


def load_stocks(filename: str) -> list[dict]:
    """Загрузить запасы."""
    return load_json(filename)


def save_stocks(filename: str, stocks: list[dict]) -> None:
    """Сохранить запасы."""
    save_json(filename, stocks)


def load_operations(filename: str) -> list[dict]:
    """Загрузить операции."""
    return load_json(filename)


def save_operations(filename: str, operations: list[dict]) -> None:
    """Сохранить операции."""
    save_json(filename, operations)
