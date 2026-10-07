from models import Category, Operation, Stock, User
from models.categories import (
    add_category,
    find_category_by_name,
    show_categories,
)
from models.users import find_user_by_id
from models.operations import (
    cancel_operation,
    consume_stock,
    get_operations_statistics,
    restock,
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
    load_operations,
    load_stocks,
    load_users,
    save_categories,
    save_operations,
    save_stocks,
    save_users,
)
from utils import input_float, input_int, input_nonempty

CATEGORIES_FILE = "data/categories.json"
USERS_FILE = "data/users.json"
STOCKS_FILE = "data/stocks.json"
OPERATIONS_FILE = "data/operations.json"


def show_stocks(stocks: list[Stock]) -> None:
    """Вывести список запасов в виде таблицы."""
    if not stocks:
        print("Список запасов пуст.")
        return
    print(f"{'ID':<4}{'Название':<20}{'Категория':<15}{'Кол-во'}")
    print("-" * 50)
    for s in stocks:
        qty = f"{s.quantity} {s.unit}"
        print(
            f"{s.id:<4}{s.name:<20}{s.category.name:<15}{qty}"
        )


def show_operations(operations: list[Operation]) -> None:
    """Вывести список операций."""
    if not operations:
        print("Операций пока нет.")
        return
    print(
        f"{'ID':<4}{'Запас':<20}{'Тип':<12}"
        f"{'Кол-во':<10}{'Дата'}"
    )
    print("-" * 60)
    for o in operations:
        print(
            f"{o.id:<4}{o.stock.name:<20}{o.type:<12}"
            f"{o.amount:<10}{o.date.isoformat()}"
        )


def show_statistics(
    stocks: list[Stock],
    operations: list[Operation],
) -> None:
    """Показать сводную статистику."""
    stat = get_statistics(stocks)
    op_stat = get_operations_statistics(operations)
    print("\n--- Статистика запасов ---")
    print(f"Всего запасов       : {stat['total']}")
    print("По категориям:")
    for cat, count in stat["by_category"].items():
        print(f"  {cat}: {count}")
    print("\n--- Статистика операций ---")
    print(f"Всего операций      : {op_stat['total']}")
    print(f"Израсходовано       : {op_stat['consumed']}")
    print(f"Пополнено           : {op_stat['restocked']}")


def menu() -> None:
    """Главное меню приложения."""
    print("\n=== Household-supplies: система контроля домашних запасов ===")
    print("1. Показать запасы")
    print("2. Добавить запас")
    print("3. Удалить запас")
    print("4. Найти запас по названию")
    print("5. Фильтр по категории")
    print("6. Отсортировать по названию")
    print("7. Списать запас")
    print("8. Пополнить запас")
    print("9. Отменить операцию")
    print("10. Показать операции")
    print("11. Статистика")
    print("12. Показать категории")
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
    owner = find_user_by_id(users, owner_id)
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
    operations = load_operations(OPERATIONS_FILE, stocks)

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
                linked = [o for o in operations if o.stock.id == stock_id]
                if linked:
                    print(
                        f"У запаса {len(linked)} связанных операций. "
                        f"Они будут удалены вместе с запасом."
                    )
                confirm = input_nonempty("Подтвердить удаление? (да/нет): ")
                if confirm.lower() in ("да", "y", "yes"):
                    deleted = delete_stock(stocks, stock_id)
                    operations[:] = [
                        o for o in operations
                        if o.stock.id != stock_id
                    ]
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
                    show_stocks(filter_stocks_by_category(stocks, category))
            elif choice == 6:
                show_stocks(sort_stocks_by_name(stocks))
            elif choice == 7:
                stock_id = input_int("ID запаса: ")
                amount = input_float("Сколько списать: ")
                consume_stock(stocks, operations, stock_id, amount)
                print("Операция выполнена.")
            elif choice == 8:
                stock_id = input_int("ID запаса: ")
                amount = input_float("Сколько пополнить: ")
                restock(stocks, operations, stock_id, amount)
                print("Операция выполнена.")
            elif choice == 9:
                op_id = input_int("ID операции: ")
                cancel_operation(operations, op_id)
                print("Операция отменена.")
            elif choice == 10:
                show_operations(operations)
            elif choice == 11:
                show_statistics(stocks, operations)
            elif choice == 12:
                show_categories(categories)
            elif choice == 0:
                save_categories(CATEGORIES_FILE, categories)
                save_users(USERS_FILE, users)
                save_stocks(STOCKS_FILE, stocks)
                save_operations(OPERATIONS_FILE, operations)
                print("Данные сохранены. До свидания!")
                break
            else:
                print("Неизвестная команда.")
        except ValueError as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
