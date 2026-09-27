from models import Category
from models.categories import add_category, find_category_by_name


def test_category_creation():
    cat = Category(1, "продукты", "Продукты питания")
    assert cat.id == 1
    assert cat.name == "продукты"


def test_is_system():
    assert Category.is_system("продукты")
    assert not Category.is_system("игрушки")


def test_find_category_by_name():
    categories = []
    add_category(categories, "продукты")
    add_category(categories, "химия")
    cat = find_category_by_name(categories, "ХИМИЯ")
    assert cat is not None
    assert cat.name == "химия"
