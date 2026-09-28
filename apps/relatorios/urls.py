from django.urls import path

from .views import RelatorioDesenvolvimentoView


app_name = "relatorios"

urlpatterns = [
    path(
        "desenvolvimento/",
        RelatorioDesenvolvimentoView.as_view(),
        name="desenvolvimento",
    ),
]
