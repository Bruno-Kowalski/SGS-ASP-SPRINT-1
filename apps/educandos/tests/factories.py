from datetime import date

from apps.educandos.models import (
    Educando,
    NucleoFamiliar,
    Responsavel,
    SituacaoSocioassistencial,
)


def gerar_cpf(numero: int) -> str:
    base = f"{numero:09d}"[-9:]
    if base == base[0] * 9:
        base = "123456789"

    digitos = [int(valor) for valor in base]
    for peso_inicial in (10, 11):
        soma = sum(valor * peso for valor, peso in zip(digitos, range(peso_inicial, 1, -1)))
        resto = soma % 11
        digitos.append(0 if resto < 2 else 11 - resto)
    return "".join(str(valor) for valor in digitos)


def criar_nucleo(sufixo="001"):
    return NucleoFamiliar.objects.create(
        identificacao=f"Núcleo Fictício {sufixo}",
        endereco=f"Endereço fictício {sufixo}",
        composicao_familiar="Composição exclusivamente fictícia para testes.",
    )


def criar_responsavel(nucleo=None, numero_cpf=123456789, nome="Responsável Teste"):
    nucleo = nucleo or criar_nucleo()
    return Responsavel.objects.create(
        nucleo_familiar=nucleo,
        nome_completo=nome,
        cpf=gerar_cpf(numero_cpf),
        contato="61999990000",
        parentesco="Responsável legal",
    )


def criar_educando(numero_cpf=987654321, nome="Educando Teste", nucleo=None):
    return Educando.objects.create(
        nome_completo=nome,
        data_nascimento=date(2012, 5, 10),
        cpf=gerar_cpf(numero_cpf),
        endereco="Endereço fictício do educando",
        contato="61988880000",
        nucleo_familiar=nucleo,
    )


def criar_situacao(educando, usuario=None, data_referencia=date(2026, 9, 20)):
    return SituacaoSocioassistencial.objects.create(
        educando=educando,
        data_referencia=data_referencia,
        situacao_socioeconomica="Situação fictícia estável para teste.",
        beneficios_sociais="Não possui, conforme massa fictícia.",
        vulnerabilidades_identificadas="Nenhuma na massa fictícia.",
        registrado_por=usuario,
    )
