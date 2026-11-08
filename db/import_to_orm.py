import os
import sys
import sqlite3
from datetime import date
from pathlib import Path
import django

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homestock.settings")
django.setup()

from categories.models import Category
from users.models import User
from stocks.models import Stock

SOURCE_DB = BASE_DIR / "data" / "homestock.sqlite"

def main():
    if not SOURCE_DB.exists():
        print("Старая база не найдена!")
        return

    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row

        categories = connection.execute("SELECT * FROM categories").fetchall()
        for row in categories:
            Category.objects.update_or_create(
                pk=row["id"],
                defaults={"name": row["name"], "description": row["description"]}
            )
        print(f"Категорий перенесено: {len(categories)}")

        users = connection.execute("SELECT * FROM users").fetchall()
        for row in users:
            User.objects.update_or_create(
                pk=row["id"],
                defaults={"name": row["name"], "email": row["email"]}
            )
        print(f"Пользователей перенесено: {len(users)}")

        stocks = connection.execute("SELECT * FROM stocks").fetchall()
        for row in stocks:
            expiry = date.fromisoformat(row["expiry_date"]) if row["expiry_date"] else None
            Stock.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "category_id": row["category_id"],
                    "owner_id": row["user_id"],
                    "quantity": row["quantity"],
                    "unit": row["unit"],
                    "expiry_date": expiry
                }
            )
        print(f"Запасов перенесено: {len(stocks)}")

if __name__ == "__main__":
    main()