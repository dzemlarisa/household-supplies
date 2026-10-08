from models import Category
from models.operations import cancel_operation, consume_stock, restock
from models.stocks import add_stock


def _prepare(name: str = "Рис", quantity: float = 2.0):
    """Создать категорию, запас и пустые коллекции."""
    category = Category(1, "продукты")
    stocks = []
    operations = []
    add_stock(stocks, name, category, quantity, "кг")
    return stocks, operations


def test_consume_stock():
    stocks, operations = _prepare()
    consume_stock(stocks, operations, 1, 0.5)
    assert stocks[0].quantity == 1.5
    assert len(operations) == 1
    assert operations[0].type == "consume"


def test_restock():
    stocks, operations = _prepare("Сахар", 0.5)
    restock(stocks, operations, 1, 1.0)
    assert stocks[0].quantity == 1.5
    assert operations[0].type == "restock"


def test_cancel_operation():
    stocks, operations = _prepare()
    op = consume_stock(stocks, operations, 1, 0.5)
    cancel_operation(operations, op.id)
    assert stocks[0].quantity == 2.0
    assert operations == []


def test_consume_too_much_raises():
    stocks, operations = _prepare()
    try:
        consume_stock(stocks, operations, 1, 5.0)
        assert False, "Ожидалась ошибка"
    except ValueError:
        assert True


def test_duplicate_booking_forbidden():
    """Списание больше остатка не выполняется."""
    stocks, operations = _prepare("Мука", 0.5)
    try:
        consume_stock(stocks, operations, 1, 5.0)
        assert False, "Ожидалась ошибка"
    except ValueError:
        assert True
