from django.db import models
from categories.models import Category
from users.models import User

class Stock(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="stocks", verbose_name="Категория")
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="stocks", verbose_name="Владелец")
    quantity = models.FloatField(verbose_name="Количество")
    unit = models.CharField(max_length=10, verbose_name="Ед. изм.")
    expiry_date = models.DateField(null=True, blank=True, verbose_name="Срок годности")

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

    class Meta:
        verbose_name = "Запас"
        verbose_name_plural = "Запасы"
        ordering = ["name"]