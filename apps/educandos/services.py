from django.core.exceptions import ValidationError
from django.db import transaction


@transaction.atomic
def salvar_nucleo_com_responsaveis(form, formset):
    nucleo = form.save()
    formset.instance = nucleo
    formset.save()
    return nucleo


@transaction.atomic
def salvar_vinculo(form):
    vinculo = form.save(commit=False)
    educando = vinculo.educando
    responsavel = vinculo.responsavel

    if educando.nucleo_familiar_id is None:
        educando.nucleo_familiar = responsavel.nucleo_familiar
    elif educando.nucleo_familiar_id != responsavel.nucleo_familiar_id:
        raise ValidationError(
            "O responsável selecionado pertence a outro núcleo familiar."
        )

    vinculo.full_clean()
    vinculo.save()

    if vinculo.principal:
        educando.responsavel_principal = responsavel

    educando.save()
    return vinculo


@transaction.atomic
def salvar_situacao(form, usuario):
    situacao = form.save(commit=False)
    situacao.registrado_por = usuario
    situacao.full_clean()
    situacao.save()
    return situacao
