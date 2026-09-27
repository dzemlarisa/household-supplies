from stocks import (
    add_stock,
    delete_stock,
    find_stock,
    sort_stocks_by_name,
)


def test_add_stock():
    stocks = []
    add_stock(stocks, "Рис", "продукты", 2.0, "кг")
    assert len(stocks) == 1
    assert stocks[0]["name"] == "Рис"


def test_delete_stock():
    stocks = []
    add_stock(stocks, "Рис", "продукты", 2.0, "кг")
    add_stock(stocks, "Сахар", "продукты", 0.5, "кг")
    deleted = delete_stock(stocks, 1)
    assert deleted["name"] == "Рис"
    assert len(stocks) == 1
    assert stocks[0]["name"] == "Сахар"


def test_delete_missing_stock():
    stocks = []
    add_stock(stocks, "Рис", "продукты", 2.0, "кг")
    try:
        delete_stock(stocks, 999)
        assert False, "Ожидалась ошибка"
    except ValueError:
        assert True


def test_find_stock():
    stocks = []
    add_stock(stocks, "Рис", "продукты", 2.0, "кг")
    add_stock(stocks, "Сахар", "продукты", 0.5, "кг")
    assert len(find_stock(stocks, "сахар")) == 1


def test_sort_by_name():
    stocks = []
    add_stock(stocks, "Рис", "продукты", 2.0, "кг")
    add_stock(stocks, "Апельсин", "продукты", 1.0, "кг")
    sorted_stocks = sort_stocks_by_name(stocks)
    assert sorted_stocks[0]["name"] == "Апельсин"
