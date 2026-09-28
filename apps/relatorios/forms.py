from django import forms

from apps.educandos.models import Educando


class DataInput(forms.DateInput):
    input_type = "date"


class RelatorioDesenvolvimentoFiltroForm(forms.Form):
    educando = forms.ModelChoiceField(
        queryset=Educando.objects.none(),
        required=False,
        empty_label="Todos os educandos",
    )
    nome = forms.CharField(
        required=False,
        max_length=150,
        label="Nome contém",
    )
    data_inicio = forms.DateField(
        required=False,
        label="Situação a partir de",
        widget=DataInput(),
    )
    data_fim = forms.DateField(
        required=False,
        label="Situação até",
        widget=DataInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["educando"].queryset = Educando.objects.order_by("nome_completo")

    def clean(self):
        dados = super().clean()
        inicio = dados.get("data_inicio")
        fim = dados.get("data_fim")
        if inicio and fim and inicio > fim:
            raise forms.ValidationError(
                "A data inicial não pode ser posterior à data final."
            )
        return dados
