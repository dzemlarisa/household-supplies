"""Операции прихода и расхода запасов."""
from datetime import date


def consume_stock(
    stocks: list[dict],
    operations: list[dict],
    stock_id: int,
    amount: float
) -> dict:
    """Списать amount единиц запаса и записать операцию.

    Возвращает словарь операции.
    """
    stock = next((s for s in stocks if s["id"] == stock_id), None)
    if stock is None:
        raise ValueError(f"Запас с id={stock_id} не найден.")
    if amount <= 0:
        raise ValueError("Количество должно быть положительным.")
    if amount > stock["quantity"]:
        raise ValueError(
            f"Недостаточно запаса: "
            f"остаток {stock['quantity']} {stock['unit']}."
        )

    stock["quantity"] = round(stock["quantity"] - amount, 2)
    op_id = max((o["id"] for o in operations), default=0) + 1
    operation = {
        "id": op_id,
        "stock_id": stock_id,
        "type": "consume",
        "amount": round(amount, 2),
        "date": date.today().isoformat(),
    }
    operations.append(operation)
    return operation


def restock(
    stocks: list[dict],
    operations: list[dict],
    stock_id: int,
    amount: float
) -> dict:
    """Пополнить запас и записать операцию."""
    stock = next((s for s in stocks if s["id"] == stock_id), None)
    if stock is None:
        raise ValueError(f"Запас с id={stock_id} не найден.")
    if amount <= 0:
        raise ValueError("Количество должно быть положительным.")

    stock["quantity"] = round(stock["quantity"] + amount, 2)
    op_id = max((o["id"] for o in operations), default=0) + 1
    operation = {
        "id": op_id,
        "stock_id": stock_id,
        "type": "restock",
        "amount": round(amount, 2),
        "date": date.today().isoformat(),
    }
    operations.append(operation)
    return operation


def cancel_operation(
    stocks: list[dict],
    operations: list[dict],
    operation_id: int
) -> None:
    """Отменить операцию и вернуть запас в исходное состояние."""
    op = next((o for o in operations if o["id"] == operation_id), None)
    if op is None:
        raise ValueError(f"Операция с id={operation_id} не найдена.")
    stock = next((s for s in stocks if s["id"] == op["stock_id"]), None)
    if stock is None:
        raise ValueError("Связанный запас не найден.")

    if op["type"] == "consume":
        stock["quantity"] = round(stock["quantity"] + op["amount"], 2)
    else:
        if stock["quantity"] < op["amount"]:
            raise ValueError(
                "Невозможно отменить пополнение: запас израсходован."
            )
        stock["quantity"] = round(stock["quantity"] - op["amount"], 2)

    operations.remove(op)


def get_operations_statistics(operations: list[dict]) -> dict:
    """Сводка по операциям."""
    consumed = sum(
        o["amount"] for o in operations if o["type"] == "consume"
    )
    restocked = sum(
        o["amount"] for o in operations if o["type"] == "restock"
    )
    return {
        "total": len(operations),
        "consumed": round(consumed, 2),
        "restocked": round(restocked, 2),
    }
