class User:
    """Пользователь системы HomeStock."""

    def __init__(
        self,
        user_id: int,
        name: str,
        email: str,
    ) -> None:
        """Создать объект пользователя."""
        self.id = user_id
        self.name = name
        self.email = email

    def __str__(self) -> str:
        """Строковое представление пользователя."""
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из данных JSON."""
        return cls(
            user_id=data["id"],
            name=data["name"],
            email=data["email"],
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }


def add_user(users: list[User], name: str, email: str) -> User:
    """Создать пользователя и добавить его в коллекцию."""
    new_id = max((u.id for u in users), default=0) + 1
    user = User(new_id, name, email)
    users.append(user)
    return user


def find_user(users: list[User], query: str) -> list[User]:
    """Найти пользователей по имени или email."""
    q = query.lower()
    return [
        u for u in users
        if q in u.name.lower() or q in u.email.lower()
    ]


def find_user_by_id(users: list[User], user_id: int) -> User | None:
    """Найти пользователя по идентификатору."""
    for u in users:
        if u.id == user_id:
            return u
    return None


def show_users(users: list[User]) -> None:
    """Вывести список пользователей."""
    if not users:
        print("Пользователей нет.")
        return
    print(f"{'ID':<4}{'Имя':<20}{'Email'}")
    print("-" * 50)
    for u in users:
        print(f"{u.id:<4}{u.name:<20}{u.email}")
