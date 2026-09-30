from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from apps.educandos.views import InicioView


urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="registration/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "",
        InicioView.as_view(),
        name="inicio",
    ),

    path(
        "educandos/",
        include("apps.educandos.urls"),
    ),

    path(
        "relatorios/",
        include("apps.relatorios.urls"),
    ),

    path(
        "__reload__/",
        include("django_browser_reload.urls"),
    ),
]