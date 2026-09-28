from django.urls import path

from .views import (
    EducandoCreateView,
    EducandoListView,
    NucleoFamiliarCreateView,
    NucleoFamiliarListView,
    SituacaoCreateView,
    SituacaoListView,
    VinculoCreateView,
    VinculoListView,
)


app_name = "educandos"

urlpatterns = [
    path("", EducandoListView.as_view(), name="educando_lista"),
    path("novo/", EducandoCreateView.as_view(), name="educando_criar"),
    path("nucleos/", NucleoFamiliarListView.as_view(), name="nucleo_lista"),
    path("nucleos/novo/", NucleoFamiliarCreateView.as_view(), name="nucleo_criar"),
    path("vinculos/", VinculoListView.as_view(), name="vinculo_lista"),
    path("vinculos/novo/", VinculoCreateView.as_view(), name="vinculo_criar"),
    path("situacoes/", SituacaoListView.as_view(), name="situacao_lista"),
    path("situacoes/nova/", SituacaoCreateView.as_view(), name="situacao_criar"),
]
