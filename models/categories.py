class Category:
    """Категория домашних запасов."""

    SYSTEM_NAMES = {"продукты", "химия", "гигиена"}

    def __init__(
        self,
        category_id: int,
        name: str,
        description: str = "",
    ) -> None:
        """Создать объект категории."""
        self.id = category_id
        self.name = name
        self.description = description

    def __str__(self) -> str:
        """Строковое представление категории."""
        return f"Category(id={self.id}, name='{self.name}')"

    @classmethod
    def from_data(cls, data: dict) -> "Category":
        """Создать категорию из данных JSON."""
        return cls(
            category_id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

    @staticmethod
    def is_system(name: str) -> bool:
        """Проверить, является ли название системным."""
        return name.lower() in Category.SYSTEM_NAMES


def add_category(
    categories: list[Category],
    name: str,
    description: str = "",
) -> Category:
    """Добавить категорию в коллекцию."""
    new_id = max((c.id for c in categories), default=0) + 1
    category = Category(new_id, name, description)
    categories.append(category)
    return category


def find_category_by_name(
    categories: list[Category],
    name: str,
) -> Category | None:
    """Найти категорию по названию."""
    name_lower = name.lower()
    for c in categories:
        if c.name.lower() == name_lower:
            return c
    return None


def find_category_by_id(
    categories: list[Category],
    category_id: int,
) -> Category | None:
    """Найти категорию по идентификатору."""
    for c in categories:
        if c.id == category_id:
            return c
    return None


def show_categories(categories: list[Category]) -> None:
    """Вывести список категорий."""
    if not categories:
        print("Категорий нет.")
        return
    print(f"{'ID':<4}{'Название':<15}{'Описание'}")
    print("-" * 50)
    for c in categories:
        print(f"{c.id:<4}{c.name:<15}{c.description}")
