from models import Category
from models.stocks import (
    add_stock,
    delete_stock,
    find_stock,
    get_statistics,
    sort_stocks_by_name,
)


def _make_category():
    return Category(1, "продукты")


def test_stock_creation():
    cat = _make_category()
    stocks = []
    stock = add_stock(stocks, "Рис", cat, 2.0, "кг")
    assert stock.id == 1
    assert stock.name == "Рис"
    assert stock.category is cat
    assert stock.quantity == 2.0


def test_find_stock():
    cat = _make_category()
    stocks = []
    add_stock(stocks, "Рис", cat, 2.0, "кг")
    add_stock(stocks, "Сахар", cat, 0.5, "кг")
    assert len(find_stock(stocks, "сахар")) == 1


def test_sort_by_name():
    cat = _make_category()
    stocks = []
    add_stock(stocks, "Рис", cat, 2.0, "кг")
    add_stock(stocks, "Апельсин", cat, 1.0, "кг")
    sorted_stocks = sort_stocks_by_name(stocks)
    assert sorted_stocks[0].name == "Апельсин"


def test_delete_stock():
    cat = _make_category()
    stocks = []
    add_stock(stocks, "Рис", cat, 2.0, "кг")
    add_stock(stocks, "Сахар", cat, 0.5, "кг")
    deleted = delete_stock(stocks, 1)
    assert deleted.name == "Рис"
    assert len(stocks) == 1
    assert stocks[0].name == "Сахар"


def test_get_statistics():
    cat = _make_category()
    stocks = []
    add_stock(stocks, "Рис", cat, 2.0, "кг")
    add_stock(stocks, "Сахар", cat, 0.5, "кг")
    stat = get_statistics(stocks)
    assert stat["total"] == 2
    assert stat["by_category"]["продукты"] == 2
