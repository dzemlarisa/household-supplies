from operations import (
    cancel_operation,
    consume_stock,
    get_operations_statistics,
    restock,
)
from stocks import (
    add_stock,
    delete_stock,
    filter_stocks_by_category,
    find_stock,
    get_statistics,
    sort_stocks_by_name,
)
from storage import (
    load_operations,
    load_stocks,
    save_operations,
    save_stocks,
)
from utils import input_float, input_int, input_nonempty

STOCKS_FILE = "data/stocks.json"
OPERATIONS_FILE = "data/operations.json"


def count_stock_operations(operations: list[dict], stock_id: int) -> int:
    """Сколько операций связано с запасом."""
    return sum(1 for o in operations if o["stock_id"] == stock_id)


def show_stocks(stocks: list[dict]) -> None:
    """Вывести список запасов в виде таблицы."""
    if not stocks:
        print("Список запасов пуст.")
        return
    print(f"{'ID':<4}{'Название':<20}{'Категория':<12}{'Кол-во':<10}")
    print("-" * 50)
    for s in stocks:
        print(
            f"{s['id']:<4}{s['name']:<20}{s['category']:<12}"
            f"{str(s['quantity']) + ' ' + s['unit']:<10}"
        )


def show_operations(operations: list[dict]) -> None:
    """Вывести список операций."""
    if not operations:
        print("Операций пока нет.")
        return
    print(f"{'ID':<4}{'Запас ID':<10}{'Тип':<12}{'Кол-во':<10}{'Дата'}")
    print("-" * 50)
    for o in operations:
        print(
            f"{o['id']:<4}{o['stock_id']:<10}{o['type']:<12}"
            f"{o['amount']:<10}{o['date']}"
        )


def show_statistics(stocks: list[dict], operations: list[dict]) -> None:
    """Показать статистику по запасам и операциям."""
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
    print("0. Выход")


def main() -> None:
    """Точка запуска приложения."""
    stocks = load_stocks(STOCKS_FILE)
    operations = load_operations(OPERATIONS_FILE)

    while True:
        menu()
        choice = input_int("Выберите действие: ")

        try:
            if choice == 1:
                show_stocks(stocks)
            elif choice == 2:
                name = input_nonempty("Название: ")
                category = input_nonempty("Категория: ").lower()
                quantity = input_float("Количество: ")
                unit = input_nonempty("Единица измерения (кг/шт/л): ")
                add_stock(stocks, name, category, quantity, unit)
                print("Запас добавлен.")
            elif choice == 3:
                stock_id = input_int("ID запаса для удаления: ")
                linked = count_stock_operations(operations, stock_id)
                if linked:
                    print(
                        f"У запаса {linked} связанных операций. "
                        f"Они будут удалены вместе с запасом."
                    )
                confirm = input_nonempty("Подтвердить удаление? (да/нет): ")
                if confirm.lower() in ("да", "y", "yes"):
                    deleted = delete_stock(stocks, stock_id)
                    operations[:] = [
                        o for o in operations
                        if o["stock_id"] != stock_id
                    ]
                    print(f"Запас «{deleted['name']}» удалён.")
                else:
                    print("Удаление отменено.")
            elif choice == 4:
                query = input_nonempty("Подстрока названия: ")
                show_stocks(find_stock(stocks, query))
            elif choice == 5:
                category = input_nonempty("Категория: ")
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
                cancel_operation(stocks, operations, op_id)
                print("Операция отменена.")
            elif choice == 10:
                show_operations(operations)
            elif choice == 11:
                show_statistics(stocks, operations)
            elif choice == 0:
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
