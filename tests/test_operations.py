from operations import cancel_operation, consume_stock, restock
from stocks import add_stock


def test_consume_stock():
    stocks = []
    operations = []
    add_stock(stocks, "Рис", "продукты", 2.0, "кг")
    consume_stock(stocks, operations, 1, 0.5)
    assert stocks[0]["quantity"] == 1.5
    assert len(operations) == 1


def test_restock():
    stocks = []
    operations = []
    add_stock(stocks, "Сахар", "продукты", 0.5, "кг")
    restock(stocks, operations, 1, 1.0)
    assert stocks[0]["quantity"] == 1.5


def test_cancel_operation():
    stocks = []
    operations = []
    add_stock(stocks, "Рис", "продукты", 2.0, "кг")
    op = consume_stock(stocks, operations, 1, 0.5)
    cancel_operation(stocks, operations, op["id"])
    assert stocks[0]["quantity"] == 2.0
    assert operations == []


def test_duplicate_booking_forbidden():
    stocks = []
    operations = []
    add_stock(stocks, "Мука", "продукты", 0.5, "кг")
    try:
        consume_stock(stocks, operations, 1, 5.0)
        assert False, "Ожидалась ошибка"
    except ValueError:
        assert True
