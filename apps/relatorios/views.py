from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView

from .forms import RelatorioDesenvolvimentoFiltroForm
from .selectors import obter_relatorio_desenvolvimento


class RelatorioDesenvolvimentoView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    TemplateView,
):
    permission_required = "educandos.view_relatorio_desenvolvimento"
    raise_exception = True
    template_name = "relatorios/desenvolvimento.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        form = RelatorioDesenvolvimentoFiltroForm(self.request.GET)
        educandos = []
        indicadores = {
            "total_educandos": 0,
            "com_nucleo_familiar": 0,
            "com_responsavel": 0,
            "com_situacao_registrada": 0,
        }

        if form.is_valid():
            educandos, indicadores = obter_relatorio_desenvolvimento(form.cleaned_data)

        contexto.update(
            {
                "form": form,
                "educandos": educandos,
                "indicadores": indicadores,
            }
        )
        return contexto
