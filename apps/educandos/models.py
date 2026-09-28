from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone

from .validators import normalizar_cpf, validar_contato, validar_cpf


class RegistroBase(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NucleoFamiliar(RegistroBase):
    identificacao = models.CharField(
        "identificação do núcleo",
        max_length=120,
        unique=True,
        help_text="Identificação interna, sem utilizar dados pessoais desnecessários.",
    )
    endereco = models.TextField("endereço")
    composicao_familiar = models.TextField(
        "composição familiar",
        help_text="Descreva resumidamente os membros que compõem o núcleo.",
    )

    class Meta:
        ordering = ["identificacao"]
        verbose_name = "núcleo familiar"
        verbose_name_plural = "núcleos familiares"

    def __str__(self):
        return self.identificacao


class Responsavel(RegistroBase):
    nucleo_familiar = models.ForeignKey(
        NucleoFamiliar,
        on_delete=models.PROTECT,
        related_name="responsaveis",
    )
    nome_completo = models.CharField("nome completo", max_length=150)
    cpf = models.CharField(
        "CPF",
        max_length=11,
        unique=True,
        validators=[validar_cpf],
    )
    contato = models.CharField(
        max_length=20,
        validators=[validar_contato],
        help_text="Telefone com DDD.",
    )
    parentesco = models.CharField(max_length=60)

    class Meta:
        ordering = ["nome_completo"]
        verbose_name = "responsável"
        verbose_name_plural = "responsáveis"

    def clean(self):
        super().clean()
        self.cpf = normalizar_cpf(self.cpf)
        validar_cpf(self.cpf)

    def save(self, *args, **kwargs):
        self.cpf = normalizar_cpf(self.cpf)
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_completo} — {self.parentesco}"


class Educando(RegistroBase):
    nome_completo = models.CharField("nome completo", max_length=150)
    data_nascimento = models.DateField("data de nascimento")
    cpf = models.CharField(
        "CPF",
        max_length=11,
        unique=True,
        validators=[validar_cpf],
    )
    endereco = models.TextField("endereço")
    contato = models.CharField(
        max_length=20,
        validators=[validar_contato],
        help_text="Telefone com DDD.",
    )
    nucleo_familiar = models.ForeignKey(
        NucleoFamiliar,
        on_delete=models.PROTECT,
        related_name="educandos",
        null=True,
        blank=True,
    )
    responsavel_principal = models.ForeignKey(
        Responsavel,
        on_delete=models.PROTECT,
        related_name="educandos_principais",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["nome_completo"]
        verbose_name = "educando"
        verbose_name_plural = "educandos"
        permissions = [
            (
                "view_relatorio_desenvolvimento",
                "Pode visualizar o relatório de desenvolvimento",
            ),
        ]

    def clean(self):
        super().clean()
        self.cpf = normalizar_cpf(self.cpf)
        validar_cpf(self.cpf)

        if self.data_nascimento and self.data_nascimento > timezone.localdate():
            raise ValidationError(
                {"data_nascimento": "A data de nascimento não pode estar no futuro."}
            )

        if (
            self.responsavel_principal_id
            and self.nucleo_familiar_id
            and self.responsavel_principal.nucleo_familiar_id != self.nucleo_familiar_id
        ):
            raise ValidationError(
                {
                    "responsavel_principal": (
                        "O responsável principal deve pertencer ao mesmo núcleo familiar."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.cpf = normalizar_cpf(self.cpf)
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_completo


class VinculoEducandoResponsavel(RegistroBase):
    class TipoVinculo(models.TextChoices):
        RESPONSAVEL_LEGAL = "RESPONSAVEL_LEGAL", "Responsável legal"
        FAMILIAR = "FAMILIAR", "Familiar"
        OUTRO = "OUTRO", "Outro responsável"

    educando = models.ForeignKey(
        Educando,
        on_delete=models.CASCADE,
        related_name="vinculos_responsaveis",
    )
    responsavel = models.ForeignKey(
        Responsavel,
        on_delete=models.PROTECT,
        related_name="vinculos_educandos",
    )
    tipo_vinculo = models.CharField(
        max_length=30,
        choices=TipoVinculo.choices,
        default=TipoVinculo.RESPONSAVEL_LEGAL,
    )
    principal = models.BooleanField(
        default=False,
        help_text="Marque quando este for o responsável principal do educando.",
    )

    class Meta:
        ordering = ["educando__nome_completo", "responsavel__nome_completo"]
        verbose_name = "vínculo entre educando e responsável"
        verbose_name_plural = "vínculos entre educandos e responsáveis"
        constraints = [
            models.UniqueConstraint(
                fields=["educando", "responsavel"],
                name="uq_educando_responsavel",
            ),
            models.UniqueConstraint(
                fields=["educando"],
                condition=Q(principal=True),
                name="uq_responsavel_principal_por_educando",
            ),
        ]

    def clean(self):
        super().clean()
        if (
            self.educando_id
            and self.responsavel_id
            and self.educando.nucleo_familiar_id
            and self.educando.nucleo_familiar_id
            != self.responsavel.nucleo_familiar_id
        ):
            raise ValidationError(
                "O educando e o responsável devem pertencer ao mesmo núcleo familiar."
            )

    def __str__(self):
        return f"{self.educando} ↔ {self.responsavel}"


class SituacaoSocioassistencial(RegistroBase):
    educando = models.ForeignKey(
        Educando,
        on_delete=models.CASCADE,
        related_name="situacoes_socioassistenciais",
    )
    data_referencia = models.DateField("data de referência", default=timezone.localdate)
    situacao_socioeconomica = models.TextField(
        "situação socioeconômica",
        help_text="Registre a situação observada no período.",
    )
    beneficios_sociais = models.TextField(
        "benefícios sociais",
        help_text="Informe os benefícios ou registre que não possui.",
    )
    vulnerabilidades_identificadas = models.TextField(
        "vulnerabilidades identificadas",
        help_text="Informe as vulnerabilidades ou registre que não foram identificadas.",
    )
    observacoes = models.TextField("observações", blank=True)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="situacoes_registradas",
        null=True,
        editable=False,
    )

    class Meta:
        ordering = ["-data_referencia", "-criado_em"]
        verbose_name = "situação socioassistencial"
        verbose_name_plural = "situações socioassistenciais"

    def clean(self):
        super().clean()
        if self.data_referencia and self.data_referencia > timezone.localdate():
            raise ValidationError(
                {"data_referencia": "A data de referência não pode estar no futuro."}
            )

    def __str__(self):
        return f"{self.educando} — {self.data_referencia:%d/%m/%Y}"
