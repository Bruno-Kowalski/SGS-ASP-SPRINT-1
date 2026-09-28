from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from apps.educandos.models import (
    Educando,
    NucleoFamiliar,
    Responsavel,
    SituacaoSocioassistencial,
    VinculoEducandoResponsavel,
)

from .factories import criar_educando, criar_nucleo, criar_responsavel, gerar_cpf


class ViewTestBase(TestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user(
            username="usuario_teste",
            password="senha-forte-para-teste",
        )
        self.client.force_login(self.usuario)

    def conceder(self, *codenames):
        permissoes = Permission.objects.filter(codename__in=codenames)
        self.usuario.user_permissions.add(*permissoes)


class EducandoViewTests(ViewTestBase):
    def test_usuario_sem_permissao_recebe_403(self):
        resposta = self.client.get(reverse("educandos:educando_criar"))
        self.assertEqual(resposta.status_code, 403)

    def test_cadastra_educando_com_permissao(self):
        self.conceder("add_educando", "view_educando")
        resposta = self.client.post(
            reverse("educandos:educando_criar"),
            {
                "nome_completo": "Educando Fictício da View",
                "data_nascimento": "2015-06-15",
                "cpf": gerar_cpf(123450001),
                "endereco": "Endereço fictício",
                "contato": "61999990000",
            },
        )
        self.assertRedirects(resposta, reverse("educandos:educando_lista"))
        self.assertEqual(Educando.objects.count(), 1)


class NucleoViewTests(ViewTestBase):
    def test_cadastra_nucleo_e_dois_responsaveis_na_mesma_operacao(self):
        self.conceder(
            "add_nucleofamiliar",
            "add_responsavel",
            "view_nucleofamiliar",
        )
        resposta = self.client.post(
            reverse("educandos:nucleo_criar"),
            {
                "identificacao": "Núcleo Fictício View",
                "endereco": "Endereço fictício",
                "composicao_familiar": "Dois responsáveis fictícios.",
                "responsaveis-TOTAL_FORMS": "2",
                "responsaveis-INITIAL_FORMS": "0",
                "responsaveis-MIN_NUM_FORMS": "1",
                "responsaveis-MAX_NUM_FORMS": "1000",
                "responsaveis-0-nome_completo": "Responsável Fictício Um",
                "responsaveis-0-cpf": gerar_cpf(123450002),
                "responsaveis-0-contato": "61999990001",
                "responsaveis-0-parentesco": "Mãe",
                "responsaveis-1-nome_completo": "Responsável Fictício Dois",
                "responsaveis-1-cpf": gerar_cpf(123450003),
                "responsaveis-1-contato": "61999990002",
                "responsaveis-1-parentesco": "Pai",
            },
        )
        self.assertRedirects(resposta, reverse("educandos:nucleo_lista"))
        self.assertEqual(NucleoFamiliar.objects.count(), 1)
        self.assertEqual(Responsavel.objects.count(), 2)

    def test_erro_em_responsavel_nao_persiste_nucleo(self):
        self.conceder("add_nucleofamiliar", "add_responsavel")
        resposta = self.client.post(
            reverse("educandos:nucleo_criar"),
            {
                "identificacao": "Núcleo Não Deve Persistir",
                "endereco": "Endereço fictício",
                "composicao_familiar": "Composição fictícia.",
                "responsaveis-TOTAL_FORMS": "2",
                "responsaveis-INITIAL_FORMS": "0",
                "responsaveis-MIN_NUM_FORMS": "1",
                "responsaveis-MAX_NUM_FORMS": "1000",
                "responsaveis-0-nome_completo": "Responsável Inválido",
                "responsaveis-0-cpf": "11111111111",
                "responsaveis-0-contato": "61999990001",
                "responsaveis-0-parentesco": "Responsável",
                "responsaveis-1-nome_completo": "",
                "responsaveis-1-cpf": "",
                "responsaveis-1-contato": "",
                "responsaveis-1-parentesco": "",
            },
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(
            NucleoFamiliar.objects.filter(
                identificacao="Núcleo Não Deve Persistir"
            ).exists()
        )


class VinculoViewTests(ViewTestBase):
    def test_nao_cria_vinculo_duplicado(self):
        self.conceder("add_vinculoeducandoresponsavel")
        nucleo = criar_nucleo("View")
        educando = criar_educando(nucleo=nucleo)
        responsavel = criar_responsavel(nucleo=nucleo)
        dados = {
            "educando": educando.pk,
            "responsavel": responsavel.pk,
            "tipo_vinculo": "RESPONSAVEL_LEGAL",
            "principal": False,
        }
        primeira = self.client.post(reverse("educandos:vinculo_criar"), dados)
        self.assertEqual(primeira.status_code, 302)
        segunda = self.client.post(reverse("educandos:vinculo_criar"), dados)
        self.assertEqual(segunda.status_code, 200)
        self.assertEqual(VinculoEducandoResponsavel.objects.count(), 1)


class SituacaoViewTests(ViewTestBase):
    def setUp(self):
        super().setUp()
        self.educando = criar_educando()

    def test_usuario_sem_permissao_nao_registra(self):
        resposta = self.client.post(
            reverse("educandos:situacao_criar"),
            {
                "educando": self.educando.pk,
                "data_referencia": "2026-09-20",
                "situacao_socioeconomica": "Situação fictícia",
                "beneficios_sociais": "Não possui",
                "vulnerabilidades_identificadas": "Nenhuma",
                "observacoes": "",
            },
        )
        self.assertEqual(resposta.status_code, 403)
        self.assertEqual(SituacaoSocioassistencial.objects.count(), 0)

    def test_usuario_autorizado_registra_com_rastreabilidade(self):
        self.conceder(
            "add_situacaosocioassistencial",
            "view_situacaosocioassistencial",
        )
        resposta = self.client.post(
            reverse("educandos:situacao_criar"),
            {
                "educando": self.educando.pk,
                "data_referencia": "2026-09-20",
                "situacao_socioeconomica": "Situação fictícia",
                "beneficios_sociais": "Não possui",
                "vulnerabilidades_identificadas": "Nenhuma",
                "observacoes": "Registro de teste.",
            },
        )
        self.assertRedirects(resposta, reverse("educandos:situacao_lista"))
        situacao = SituacaoSocioassistencial.objects.get()
        self.assertEqual(situacao.registrado_por, self.usuario)
