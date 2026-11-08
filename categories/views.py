from django.shortcuts import render
from .models import Category

def categories_list(request):
    """Страница со списком всех категорий."""
    categories = Category.objects.all()
    return render(request, "categories/category_list.html", {"categories": categories})