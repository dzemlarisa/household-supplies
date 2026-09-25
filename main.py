import math  

print("=== Household supplies: добавление нового запаса ===")

user_name = input("Введите имя пользователя: ").strip()
category = input("Категория (продукты/химия/гигиена): ").strip().lower()
item_name = input("Название запаса: ").strip()

quantity = float(input("Текущее количество: ").replace(",","."))
unit = input("Единица измерения (кг/шт/л): ").strip()

rounded_qty = math.floor(quantity * 100) / 100

print("\n--- Карточка запаса ---")
print(f"Пользователь : {user_name}")
print(f"Категория    : {category}")
print(f"Запас        : {item_name}")
print(f"Количество   : {rounded_qty} {unit}")
