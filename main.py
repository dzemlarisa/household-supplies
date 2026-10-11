from models import Category, Stock, User
from models.categories import (
    add_category,
    find_category_by_name,
    show_categories,
)
from models.stocks import (
    add_stock,
    delete_stock,
    filter_stocks_by_category,
    find_stock,
    get_statistics,
    sort_stocks_by_name,
)
from storage import (
    load_categories,
    load_stocks,
    load_users,
    save_categories,
    save_stocks,
    save_users,
)
from utils import input_float, input_int, input_nonempty

CATEGORIES_FILE = "data/categories.json"
USERS_FILE = "data/users.json"
STOCKS_FILE = "data/stocks.json"


def show_stocks(stocks: list[Stock]) -> None:
    """Вывести список запасов."""
    if not stocks:
        print("Список запасов пуст.")
        return
    print(f"{'ID':<4}{'Название':<20}{'Категория':<15}{'Кол-во'}")
    print("-" * 60)
    for s in stocks:
        qty = f"{s.quantity} {s.unit}"
        print(f"{s.id:<4}{s.name:<20}{s.category.name:<15}{qty}")


def show_statistics(stocks: list[Stock]) -> None:
    """Показать статистику по запасам."""
    stat = get_statistics(stocks)
    print("\n--- Статистика запасов ---")
    print(f"Всего запасов       : {stat['total']}")
    print("По категориям:")
    for cat, count in stat["by_category"].items():
        print(f"  {cat}: {count}")


def menu() -> None:
    """Главное меню приложения."""
    print("\n=== HomeStock: система контроля домашних запасов ===")
    print("1. Показать запасы")
    print("2. Добавить запас")
    print("3. Удалить запас")
    print("4. Найти запас по названию")
    print("5. Фильтр по категории")
    print("6. Отсортировать по названию")
    print("7. Статистика")
    print("8. Показать категории")
    print("0. Выход")


def create_new_stock(
    stocks: list[Stock],
    categories: list[Category],
    users: list[User],
) -> None:
    """Сценарий добавления запаса."""
    if not users:
        print("Сначала добавьте хотя бы одного пользователя.")
        return
    name = input_nonempty("Название: ")
    cat_name = input_nonempty("Категория: ").lower()
    category = find_category_by_name(categories, cat_name)
    if category is None:
        print(f"Категория '{cat_name}' не найдена, создаю новую.")
        category = add_category(categories, cat_name)

    print("Выберите владельца:")
    for u in users:
        print(f"  {u.id}: {u.name}")
    owner_id = input_int("ID владельца: ")
    owner = next((u for u in users if u.id == owner_id), None)
    if owner is None:
        print("Пользователь не найден.")
        return

    quantity = input_float("Количество: ")
    unit = input_nonempty("Единица измерения (кг/шт/л): ")
    add_stock(stocks, name, category, owner, quantity, unit)
    print(f"Запас «{name}» добавлен пользователю {owner.name}.")


def main() -> None:
    """Точка запуска приложения."""
    categories = load_categories(CATEGORIES_FILE)
    users = load_users(USERS_FILE)
    stocks = load_stocks(STOCKS_FILE, categories, users)

    while True:
        menu()
        choice = input_int("Выберите действие: ")
        try:
            if choice == 1:
                show_stocks(stocks)
            elif choice == 2:
                create_new_stock(stocks, categories, users)
            elif choice == 3:
                stock_id = input_int("ID запаса для удаления: ")
                confirm = input_nonempty(
                    "Подтвердить удаление? (да/нет): "
                )
                if confirm.lower() in ("да", "y", "yes"):
                    deleted = delete_stock(stocks, stock_id)
                    print(f"Запас «{deleted.name}» удалён.")
                else:
                    print("Удаление отменено.")
            elif choice == 4:
                query = input_nonempty("Подстрока названия: ")
                show_stocks(find_stock(stocks, query))
            elif choice == 5:
                cat_name = input_nonempty("Категория: ")
                category = find_category_by_name(categories, cat_name)
                if category is None:
                    print("Категория не найдена.")
                else:
                    show_stocks(
                        filter_stocks_by_category(stocks, category)
                    )
            elif choice == 6:
                show_stocks(sort_stocks_by_name(stocks))
            elif choice == 7:
                show_statistics(stocks)
            elif choice == 8:
                show_categories(categories)
            elif choice == 0:
                save_categories(CATEGORIES_FILE, categories)
                save_users(USERS_FILE, users)
                save_stocks(STOCKS_FILE, stocks)
                print("Данные сохранены. До свидания!")
                break
            else:
                print("Неизвестная команда.")
        except ValueError as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
