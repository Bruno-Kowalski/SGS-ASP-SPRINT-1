from django import forms
from django.forms import inlineformset_factory

from .models import (
    Educando,
    NucleoFamiliar,
    Responsavel,
    SituacaoSocioassistencial,
    VinculoEducandoResponsavel,
)
from .validators import normalizar_cpf


class DataInput(forms.DateInput):
    input_type = "date"


class EducandoForm(forms.ModelForm):
    cpf = forms.CharField(
        max_length=14,
        label="CPF",
        help_text="Pode ser informado com ou sem pontuação.",
    )

    class Meta:
        model = Educando
        fields = ["nome_completo", "data_nascimento", "cpf", "endereco", "contato"]
        widgets = {
            "data_nascimento": DataInput(),
            "endereco": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_cpf(self):
        return normalizar_cpf(self.cleaned_data["cpf"])


class NucleoFamiliarForm(forms.ModelForm):
    class Meta:
        model = NucleoFamiliar
        fields = ["identificacao", "endereco", "composicao_familiar"]
        widgets = {
            "endereco": forms.Textarea(attrs={"rows": 3}),
            "composicao_familiar": forms.Textarea(attrs={"rows": 3}),
        }


class ResponsavelForm(forms.ModelForm):
    cpf = forms.CharField(
        max_length=14,
        label="CPF",
        help_text="Pode ser informado com ou sem pontuação.",
    )

    class Meta:
        model = Responsavel
        fields = ["nome_completo", "cpf", "contato", "parentesco"]

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        return normalizar_cpf(cpf) if cpf else cpf


ResponsavelFormSet = inlineformset_factory(
    NucleoFamiliar,
    Responsavel,
    form=ResponsavelForm,
    extra=2,
    min_num=1,
    validate_min=True,
    can_delete=False,
)


class VinculoEducandoResponsavelForm(forms.ModelForm):
    class Meta:
        model = VinculoEducandoResponsavel
        fields = ["educando", "responsavel", "tipo_vinculo", "principal"]

    def clean(self):
        dados = super().clean()
        educando = dados.get("educando")
        responsavel = dados.get("responsavel")
        principal = dados.get("principal")

        if (
            educando
            and responsavel
            and educando.nucleo_familiar_id
            and educando.nucleo_familiar_id != responsavel.nucleo_familiar_id
        ):
            self.add_error(
                "responsavel",
                "Selecione um responsável do mesmo núcleo familiar do educando.",
            )

        if (
            principal
            and educando
            and VinculoEducandoResponsavel.objects.filter(
                educando=educando,
                principal=True,
            )
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            self.add_error(
                "principal",
                "Este educando já possui um responsável principal.",
            )

        return dados


class SituacaoSocioassistencialForm(forms.ModelForm):
    class Meta:
        model = SituacaoSocioassistencial
        fields = [
            "educando",
            "data_referencia",
            "situacao_socioeconomica",
            "beneficios_sociais",
            "vulnerabilidades_identificadas",
            "observacoes",
        ]
        widgets = {
            "data_referencia": DataInput(),
            "situacao_socioeconomica": forms.Textarea(attrs={"rows": 3}),
            "beneficios_sociais": forms.Textarea(attrs={"rows": 3}),
            "vulnerabilidades_identificadas": forms.Textarea(attrs={"rows": 3}),
            "observacoes": forms.Textarea(attrs={"rows": 3}),
        }
