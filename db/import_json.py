import json
from db.database import get_connection

CATEGORIES_FILE = "data/categories.json"
USERS_FILE = "data/users.json"
STOCKS_FILE = "data/stocks.json"

def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)

def import_data():
    conn = get_connection()
    try:
        conn.execute("DELETE FROM stocks")
        conn.execute("DELETE FROM users")
        conn.execute("DELETE FROM categories")

        categories = load_json(CATEGORIES_FILE)
        conn.executemany(
            "INSERT INTO categories (id, name, description) VALUES (?, ?, ?)",
            [(c["id"], c["name"], c.get("description", "")) for c in categories]
        )

        users = load_json(USERS_FILE)
        conn.executemany(
            "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
            [(u["id"], u["name"], u["email"]) for u in users]
        )

        stocks = load_json(STOCKS_FILE)
        conn.executemany(
            """INSERT INTO stocks 
               (id, category_id, user_id, name, quantity, unit, expiry_date) 
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [(s["id"], s["category_id"], s["user_id"], s["name"], s["quantity"], s["unit"], s.get("expiry_date")) for s in stocks]
        )
        
        conn.commit()
        print("Данные успешно импортированы!")
    except Exception as e:
        conn.rollback()
        print("Ошибка импорта:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    import_data()