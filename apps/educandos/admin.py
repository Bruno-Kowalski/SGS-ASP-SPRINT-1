from django.contrib import admin

from .models import (
    Educando,
    NucleoFamiliar,
    Responsavel,
    SituacaoSocioassistencial,
    VinculoEducandoResponsavel,
)


class ResponsavelInline(admin.TabularInline):
    model = Responsavel
    extra = 0


@admin.register(NucleoFamiliar)
class NucleoFamiliarAdmin(admin.ModelAdmin):
    list_display = ("identificacao", "criado_em", "atualizado_em")
    search_fields = ("identificacao",)
    inlines = [ResponsavelInline]
    readonly_fields = ("criado_em", "atualizado_em")


@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ("nome_completo", "parentesco", "nucleo_familiar", "contato")
    list_filter = ("parentesco", "nucleo_familiar")
    search_fields = ("nome_completo", "cpf")
    readonly_fields = ("criado_em", "atualizado_em")


@admin.register(Educando)
class EducandoAdmin(admin.ModelAdmin):
    list_display = (
        "nome_completo",
        "data_nascimento",
        "nucleo_familiar",
        "responsavel_principal",
    )
    list_filter = ("nucleo_familiar",)
    search_fields = ("nome_completo", "cpf")
    readonly_fields = ("criado_em", "atualizado_em")


@admin.register(VinculoEducandoResponsavel)
class VinculoAdmin(admin.ModelAdmin):
    list_display = ("educando", "responsavel", "tipo_vinculo", "principal")
    list_filter = ("tipo_vinculo", "principal")
    readonly_fields = ("criado_em", "atualizado_em")


@admin.register(SituacaoSocioassistencial)
class SituacaoSocioassistencialAdmin(admin.ModelAdmin):
    list_display = ("educando", "data_referencia", "registrado_por")
    list_filter = ("data_referencia",)
    search_fields = ("educando__nome_completo",)
    readonly_fields = ("registrado_por", "criado_em", "atualizado_em")

    def save_model(self, request, obj, form, change):
        if obj.registrado_por_id is None:
            obj.registrado_por = request.user
        super().save_model(request, obj, form, change)


admin.site.site_header = "SGS-ASP — Administração"
admin.site.site_title = "SGS-ASP"
admin.site.index_title = "Gestão da Sprint 1"
