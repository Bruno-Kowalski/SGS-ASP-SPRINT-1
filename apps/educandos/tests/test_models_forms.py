from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from apps.educandos.forms import EducandoForm, ResponsavelFormSet
from apps.educandos.models import (
    Educando,
    NucleoFamiliar,
    SituacaoSocioassistencial,
    VinculoEducandoResponsavel,
)
from apps.educandos.services import salvar_vinculo

from .factories import criar_educando, criar_nucleo, criar_responsavel, gerar_cpf


class EducandoModelFormTests(TestCase):
    def test_cadastra_educando_valido_e_normaliza_cpf(self):
        cpf = gerar_cpf(123456780)
        cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        form = EducandoForm(
            data={
                "nome_completo": "Educando Fictício Um",
                "data_nascimento": "2014-03-12",
                "cpf": cpf_formatado,
                "endereco": "Endereço fictício",
                "contato": "(61) 99999-0000",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        educando = form.save()
        self.assertEqual(educando.cpf, cpf)
        self.assertTrue(Educando.objects.filter(pk=educando.pk).exists())

    def test_bloqueia_cpf_invalido(self):
        form = EducandoForm(
            data={
                "nome_completo": "Educando Fictício",
                "data_nascimento": "2014-03-12",
                "cpf": "111.111.111-11",
                "endereco": "Endereço fictício",
                "contato": "61999990000",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("cpf", form.errors)

    def test_bloqueia_campos_obrigatorios_vazios(self):
        form = EducandoForm(data={})
        self.assertFalse(form.is_valid())
        for campo in ("nome_completo", "data_nascimento", "cpf", "endereco", "contato"):
            self.assertIn(campo, form.errors)

    def test_bloqueia_cpf_duplicado(self):
        existente = criar_educando(numero_cpf=123456701)
        form = EducandoForm(
            data={
                "nome_completo": "Outro Educando Fictício",
                "data_nascimento": "2013-02-11",
                "cpf": existente.cpf,
                "endereco": "Outro endereço fictício",
                "contato": "61977770000",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("cpf", form.errors)

    def test_bloqueia_data_de_nascimento_futura(self):
        educando = criar_educando()
        educando.data_nascimento = timezone.localdate() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            educando.save()


class NucleoFamiliarTests(TestCase):
    def test_formset_exige_ao_menos_um_responsavel(self):
        nucleo = NucleoFamiliar()
        formset = ResponsavelFormSet(
            data={
                "responsaveis-TOTAL_FORMS": "2",
                "responsaveis-INITIAL_FORMS": "0",
                "responsaveis-MIN_NUM_FORMS": "1",
                "responsaveis-MAX_NUM_FORMS": "1000",
                "responsaveis-0-nome_completo": "",
                "responsaveis-0-cpf": "",
                "responsaveis-0-contato": "",
                "responsaveis-0-parentesco": "",
                "responsaveis-1-nome_completo": "",
                "responsaveis-1-cpf": "",
                "responsaveis-1-contato": "",
                "responsaveis-1-parentesco": "",
            },
            instance=nucleo,
            prefix="responsaveis",
        )
        self.assertFalse(formset.is_valid())
        self.assertTrue(formset.non_form_errors())


class VinculoTests(TestCase):
    def test_vinculo_define_nucleo_e_responsavel_principal(self):
        nucleo = criar_nucleo("A")
        responsavel = criar_responsavel(nucleo=nucleo)
        educando = criar_educando(nucleo=None)

        from apps.educandos.forms import VinculoEducandoResponsavelForm

        form = VinculoEducandoResponsavelForm(
            data={
                "educando": educando.pk,
                "responsavel": responsavel.pk,
                "tipo_vinculo": "RESPONSAVEL_LEGAL",
                "principal": True,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        salvar_vinculo(form)
        educando.refresh_from_db()
        self.assertEqual(educando.nucleo_familiar, nucleo)
        self.assertEqual(educando.responsavel_principal, responsavel)

    def test_bloqueia_vinculo_entre_nucleos_diferentes(self):
        nucleo_a = criar_nucleo("A")
        nucleo_b = criar_nucleo("B")
        educando = criar_educando(nucleo=nucleo_a)
        responsavel = criar_responsavel(nucleo=nucleo_b)
        vinculo = VinculoEducandoResponsavel(
            educando=educando,
            responsavel=responsavel,
        )
        with self.assertRaises(ValidationError):
            vinculo.full_clean()

    def test_constraint_bloqueia_vinculo_duplicado(self):
        nucleo = criar_nucleo("A")
        educando = criar_educando(nucleo=nucleo)
        responsavel = criar_responsavel(nucleo=nucleo)
        VinculoEducandoResponsavel.objects.create(
            educando=educando,
            responsavel=responsavel,
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            VinculoEducandoResponsavel.objects.create(
                educando=educando,
                responsavel=responsavel,
            )


class SituacaoSocioassistencialTests(TestCase):
    def test_bloqueia_data_futura(self):
        situacao = SituacaoSocioassistencial(
            educando=criar_educando(),
            data_referencia=timezone.localdate() + timedelta(days=1),
            situacao_socioeconomica="Situação fictícia",
            beneficios_sociais="Não possui",
            vulnerabilidades_identificadas="Nenhuma identificada",
        )
        with self.assertRaises(ValidationError):
            situacao.full_clean()
