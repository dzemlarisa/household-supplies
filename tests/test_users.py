from models import User
from models.users import add_user, find_user


def test_user_creation():
    user = User(1, "Иван Петров", "ivan@example.com")
    assert user.id == 1
    assert user.name == "Иван Петров"
    assert user.email == "ivan@example.com"


def test_user_str():
    user = User(1, "Иван Петров", "ivan@example.com")
    assert "Иван Петров" in str(user)
    assert "ivan@example.com" in str(user)


def test_user_from_data():
    data = {"id": 2, "name": "Анна", "email": "anna@example.com"}
    user = User.from_data(data)
    assert user.id == 2
    assert user.name == "Анна"


def test_add_and_find_user():
    users = []
    add_user(users, "Иван", "ivan@example.com")
    add_user(users, "Анна", "anna@example.com")
    assert len(find_user(users, "анна")) == 1
    assert len(find_user(users, "example.com")) == 2
