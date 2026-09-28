from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from apps.educandos.models import VinculoEducandoResponsavel
from apps.educandos.tests.factories import (
    criar_educando,
    criar_nucleo,
    criar_responsavel,
    criar_situacao,
)


class RelatorioDesenvolvimentoTests(TestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user(
            username="relatorio_teste",
            password="senha-forte-para-teste",
        )
        self.client.force_login(self.usuario)
        self.url = reverse("relatorios:desenvolvimento")

        self.nucleo = criar_nucleo("Relatório")
        self.responsavel = criar_responsavel(
            nucleo=self.nucleo,
            numero_cpf=321654987,
        )
        self.educando_completo = criar_educando(
            numero_cpf=789456123,
            nome="Educando Alfa",
            nucleo=self.nucleo,
        )
        VinculoEducandoResponsavel.objects.create(
            educando=self.educando_completo,
            responsavel=self.responsavel,
            principal=True,
        )
        self.educando_completo.responsavel_principal = self.responsavel
        self.educando_completo.save()
        criar_situacao(
            self.educando_completo,
            self.usuario,
            date(2026, 9, 20),
        )
        self.educando_sem_dados = criar_educando(
            numero_cpf=789456124,
            nome="Educando Beta",
        )

    def conceder_permissao(self):
        permissao = Permission.objects.get(
            codename="view_relatorio_desenvolvimento"
        )
        self.usuario.user_permissions.add(permissao)

    def test_bloqueia_usuario_sem_permissao(self):
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code, 403)

    def test_apresenta_indicadores_definidos_na_sprint_1(self):
        self.conceder_permissao()
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code, 200)
        indicadores = resposta.context["indicadores"]
        self.assertEqual(indicadores["total_educandos"], 2)
        self.assertEqual(indicadores["com_nucleo_familiar"], 1)
        self.assertEqual(indicadores["com_responsavel"], 1)
        self.assertEqual(indicadores["com_situacao_registrada"], 1)

    def test_filtro_por_nome_retorna_somente_recorte(self):
        self.conceder_permissao()
        resposta = self.client.get(self.url, {"nome": "Alfa"})
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(list(resposta.context["educandos"]), [self.educando_completo])

    def test_filtro_sem_resultado_exibe_estado_vazio(self):
        self.conceder_permissao()
        resposta = self.client.get(self.url, {"nome": "Inexistente"})
        self.assertContains(
            resposta,
            "Nenhum resultado encontrado para os filtros informados.",
        )

    def test_periodo_invalido_e_tratado_sem_executar_consulta(self):
        self.conceder_permissao()
        resposta = self.client.get(
            self.url,
            {"data_inicio": "2026-09-25", "data_fim": "2026-09-01"},
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(resposta.context["form"].is_valid())
        self.assertEqual(resposta.context["educandos"], [])
