from datetime import date

from .stocks import Stock, find_stock_by_id


class Operation:
    """Операция прихода или расхода запаса."""

    CONSUME = "consume"
    RESTOCK = "restock"

    def __init__(
        self,
        operation_id: int,
        stock: Stock,
        type_: str,
        amount: float,
        operation_date: date | None = None,
    ) -> None:
        """Создать операцию."""
        if type_ not in (Operation.CONSUME, Operation.RESTOCK):
            raise ValueError(f"Неизвестный тип операции: {type_}")
        self.id = operation_id
        self.stock = stock
        self.type = type_
        self.amount = round(amount, 2)
        self.date = operation_date or date.today()

    def __str__(self) -> str:
        """Строковое представление операции."""
        return (
            f"Operation(id={self.id}, stock='{self.stock.name}', "
            f"type='{self.type}', amount={self.amount}, "
            f"date='{self.date.isoformat()}')"
        )

    def apply(self) -> None:
        """Применить операцию к связанному запасу."""
        delta = -self.amount if self.type == Operation.CONSUME else self.amount
        self.stock.change_quantity(delta)

    def rollback(self) -> None:
        """Откатить операцию."""
        delta = self.amount if self.type == Operation.CONSUME else -self.amount
        self.stock.change_quantity(delta)

    @classmethod
    def from_data(
        cls,
        data: dict,
        stocks: list[Stock],
    ) -> "Operation":
        """Создать операцию из данных JSON, связав её с запасом."""
        stock = find_stock_by_id(stocks, data["stock_id"])
        if stock is None:
            raise ValueError(
                f"Запас id={data['stock_id']} не найден."
            )
        return cls(
            operation_id=data["id"],
            stock=stock,
            type_=data["type"],
            amount=data["amount"],
            operation_date=date.fromisoformat(data["date"]),
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "stock_id": self.stock.id,
            "type": self.type,
            "amount": self.amount,
            "date": self.date.isoformat(),
        }


def consume_stock(
    stocks: list[Stock],
    operations: list[Operation],
    stock_id: int,
    amount: float,
) -> Operation:
    """Создать операцию списания и применить её."""
    stock = find_stock_by_id(stocks, stock_id)
    if stock is None:
        raise ValueError(f"Запас id={stock_id} не найден.")
    if amount <= 0:
        raise ValueError("Количество должно быть положительным.")
    if amount > stock.quantity:
        raise ValueError(
            f"Недостаточно запаса: остаток {stock.quantity} {stock.unit}."
        )

    new_id = max((o.id for o in operations), default=0) + 1
    op = Operation(new_id, stock, Operation.CONSUME, amount)
    op.apply()
    operations.append(op)
    return op


def restock(
    stocks: list[Stock],
    operations: list[Operation],
    stock_id: int,
    amount: float,
) -> Operation:
    """Создать операцию пополнения и применить её."""
    stock = find_stock_by_id(stocks, stock_id)
    if stock is None:
        raise ValueError(f"Запас id={stock_id} не найден.")
    if amount <= 0:
        raise ValueError("Количество должно быть положительным.")

    new_id = max((o.id for o in operations), default=0) + 1
    op = Operation(new_id, stock, Operation.RESTOCK, amount)
    op.apply()
    operations.append(op)
    return op


def cancel_operation(
    operations: list[Operation],
    operation_id: int,
) -> None:
    """Отменить операцию и удалить её из коллекции."""
    op = next((o for o in operations if o.id == operation_id), None)
    if op is None:
        raise ValueError(f"Операция id={operation_id} не найдена.")
    op.rollback()
    operations.remove(op)


def find_operation_by_id(operations, operation_id):
    for o in operations:
        if o.id == operation_id:
            return o
    return None


def get_operations_statistics(operations: list[Operation]) -> dict:
    """Сводка по операциям."""
    consumed = sum(
        o.amount for o in operations if o.type == Operation.CONSUME
    )
    restocked = sum(
        o.amount for o in operations if o.type == Operation.RESTOCK
    )
    return {
        "total": len(operations),
        "consumed": round(consumed, 2),
        "restocked": round(restocked, 2),
    }
