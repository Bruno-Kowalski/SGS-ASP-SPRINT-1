from django.db.models import Prefetch

from apps.educandos.models import Educando, SituacaoSocioassistencial


def obter_relatorio_desenvolvimento(filtros):
    queryset = Educando.objects.select_related(
        "nucleo_familiar",
        "responsavel_principal",
    ).prefetch_related("vinculos_responsaveis__responsavel")

    situacoes = SituacaoSocioassistencial.objects.select_related("registrado_por").order_by(
        "-data_referencia",
        "-criado_em",
    )

    educando = filtros.get("educando")
    nome = filtros.get("nome")
    data_inicio = filtros.get("data_inicio")
    data_fim = filtros.get("data_fim")
    filtros_situacao = {}

    if educando:
        queryset = queryset.filter(pk=educando.pk)
    if nome:
        queryset = queryset.filter(nome_completo__icontains=nome.strip())
    if data_inicio:
        filtros_situacao[
            "situacoes_socioassistenciais__data_referencia__gte"
        ] = data_inicio
        situacoes = situacoes.filter(data_referencia__gte=data_inicio)
    if data_fim:
        filtros_situacao[
            "situacoes_socioassistenciais__data_referencia__lte"
        ] = data_fim
        situacoes = situacoes.filter(data_referencia__lte=data_fim)

    if filtros_situacao:
        queryset = queryset.filter(**filtros_situacao)

    queryset = queryset.distinct().prefetch_related(
        Prefetch(
            "situacoes_socioassistenciais",
            queryset=situacoes,
            to_attr="situacoes_filtradas",
        )
    )

    ids = list(queryset.values_list("pk", flat=True))
    base = Educando.objects.filter(pk__in=ids)
    indicadores = {
        "total_educandos": len(ids),
        "com_nucleo_familiar": base.filter(nucleo_familiar__isnull=False).count(),
        "com_responsavel": base.filter(
            vinculos_responsaveis__isnull=False
        ).distinct().count(),
        "com_situacao_registrada": (
            base.filter(**filtros_situacao).distinct().count()
            if filtros_situacao
            else base.filter(
                situacoes_socioassistenciais__isnull=False
            ).distinct().count()
        ),
    }

    return queryset, indicadores
