from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("stocks/", include("stocks.urls")),
    path("users/", include("users.urls")),
]

handler404 = "homepage.views.page_not_found"
