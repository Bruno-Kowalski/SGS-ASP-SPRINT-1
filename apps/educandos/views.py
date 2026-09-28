from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView

from .forms import (
    EducandoForm,
    NucleoFamiliarForm,
    ResponsavelFormSet,
    SituacaoSocioassistencialForm,
    VinculoEducandoResponsavelForm,
)
from .models import (
    Educando,
    NucleoFamiliar,
    SituacaoSocioassistencial,
    VinculoEducandoResponsavel,
)
from .services import (
    salvar_nucleo_com_responsaveis,
    salvar_situacao,
    salvar_vinculo,
)


class PermissaoObrigatoriaMixin(PermissionRequiredMixin):
    raise_exception = True


class InicioView(LoginRequiredMixin, TemplateView):
    template_name = "inicio.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto.update(
            {
                "total_educandos": Educando.objects.count(),
                "total_nucleos": NucleoFamiliar.objects.count(),
                "total_vinculos": VinculoEducandoResponsavel.objects.count(),
                "total_situacoes": SituacaoSocioassistencial.objects.count(),
            }
        )
        return contexto


class EducandoListView(LoginRequiredMixin, PermissaoObrigatoriaMixin, ListView):
    permission_required = "educandos.view_educando"
    model = Educando
    template_name = "educandos/educando_lista.html"
    context_object_name = "educandos"
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().select_related(
            "nucleo_familiar",
            "responsavel_principal",
        )


class EducandoCreateView(LoginRequiredMixin, PermissaoObrigatoriaMixin, CreateView):
    permission_required = "educandos.add_educando"
    model = Educando
    form_class = EducandoForm
    template_name = "educandos/formulario.html"
    success_url = reverse_lazy("educandos:educando_lista")
    extra_context = {
        "titulo": "Cadastrar educando",
        "subtitulo": "RF01 — Informações pessoais do educando",
    }

    def form_valid(self, form):
        messages.success(self.request, "Educando cadastrado com sucesso.")
        return super().form_valid(form)


class NucleoFamiliarListView(LoginRequiredMixin, PermissaoObrigatoriaMixin, ListView):
    permission_required = "educandos.view_nucleofamiliar"
    model = NucleoFamiliar
    template_name = "educandos/nucleo_lista.html"
    context_object_name = "nucleos"
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().prefetch_related("responsaveis")


class NucleoFamiliarCreateView(LoginRequiredMixin, PermissaoObrigatoriaMixin, View):
    permission_required = (
        "educandos.add_nucleofamiliar",
        "educandos.add_responsavel",
    )
    template_name = "educandos/nucleo_formulario.html"

    def get(self, request):
        nucleo = NucleoFamiliar()
        return render(
            request,
            self.template_name,
            {
                "form": NucleoFamiliarForm(instance=nucleo),
                "formset": ResponsavelFormSet(instance=nucleo, prefix="responsaveis"),
            },
        )

    def post(self, request):
        nucleo = NucleoFamiliar()
        form = NucleoFamiliarForm(request.POST, instance=nucleo)
        formset = ResponsavelFormSet(
            request.POST,
            instance=nucleo,
            prefix="responsaveis",
        )

        if form.is_valid() and formset.is_valid():
            salvar_nucleo_com_responsaveis(form, formset)
            messages.success(
                request,
                "Núcleo familiar e responsáveis cadastrados com sucesso.",
            )
            return redirect("educandos:nucleo_lista")

        return render(
            request,
            self.template_name,
            {"form": form, "formset": formset},
        )


class VinculoListView(LoginRequiredMixin, PermissaoObrigatoriaMixin, ListView):
    permission_required = "educandos.view_vinculoeducandoresponsavel"
    model = VinculoEducandoResponsavel
    template_name = "educandos/vinculo_lista.html"
    context_object_name = "vinculos"
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().select_related("educando", "responsavel")


class VinculoCreateView(LoginRequiredMixin, PermissaoObrigatoriaMixin, View):
    permission_required = "educandos.add_vinculoeducandoresponsavel"
    template_name = "educandos/formulario.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "form": VinculoEducandoResponsavelForm(),
                "titulo": "Vincular educando ao responsável",
                "subtitulo": "RF03 — Selecione registros existentes",
            },
        )

    def post(self, request):
        form = VinculoEducandoResponsavelForm(request.POST)
        if form.is_valid():
            try:
                salvar_vinculo(form)
            except ValidationError as erro:
                form.add_error(None, erro)
            else:
                messages.success(request, "Vínculo criado com sucesso.")
                return redirect("educandos:vinculo_lista")

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "titulo": "Vincular educando ao responsável",
                "subtitulo": "RF03 — Selecione registros existentes",
            },
        )


class SituacaoListView(LoginRequiredMixin, PermissaoObrigatoriaMixin, ListView):
    permission_required = "educandos.view_situacaosocioassistencial"
    model = SituacaoSocioassistencial
    template_name = "educandos/situacao_lista.html"
    context_object_name = "situacoes"
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().select_related("educando", "registrado_por")


class SituacaoCreateView(LoginRequiredMixin, PermissaoObrigatoriaMixin, View):
    permission_required = "educandos.add_situacaosocioassistencial"
    template_name = "educandos/formulario.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "form": SituacaoSocioassistencialForm(),
                "titulo": "Registrar situação socioassistencial",
                "subtitulo": "RF04 — Utilize apenas dados autorizados",
            },
        )

    def post(self, request):
        form = SituacaoSocioassistencialForm(request.POST)
        if form.is_valid():
            salvar_situacao(form, request.user)
            messages.success(
                request,
                "Situação socioassistencial registrada com sucesso.",
            )
            return redirect("educandos:situacao_lista")

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "titulo": "Registrar situação socioassistencial",
                "subtitulo": "RF04 — Utilize apenas dados autorizados",
            },
        )
