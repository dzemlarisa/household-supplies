from django.http import HttpResponse, HttpRequest

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/"
    "bootstrap.min.css"
)


def page(title: str, content: str) -> str:
    """Собрать HTML-страницу с общим каркасом."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link href="{BOOTSTRAP_CSS}" rel="stylesheet">
</head>
<body class="bg-light">
<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
  <div class="container">
    <a class="navbar-brand" href="/">HomeStock</a>
    <div class="navbar-nav">
      <a class="nav-link" href="/stocks/">Запасы</a>
      <a class="nav-link" href="/operations/">Операции</a>
    </div>
  </div>
</nav>
<div class="container">
{content}
</div>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница."""
    content = """
<h1 class="display-4">HomeStock</h1>
<p class="lead">Система контроля домашних запасов.</p>
<p>Основные разделы:</p>
<a href="/stocks/" class="btn btn-primary me-2">Запасы</a>
<a href="/operations/" class="btn btn-secondary">Операции</a>
"""
    return HttpResponse(page("HomeStock", content))


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Собственная страница ошибки 404."""
    content = """
<h1 class="text-danger">404 — страница не найдена</h1>
<p>Проверьте адрес или вернитесь на главную.</p>
<a href="/" class="btn btn-primary">На главную</a>
"""
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )
