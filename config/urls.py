from django.contrib import admin
from django.urls import include, path

from apps.educandos.views import InicioView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", InicioView.as_view(), name="inicio"),
    path("educandos/", include("apps.educandos.urls")),
    path("relatorios/", include("apps.relatorios.urls")),
]
