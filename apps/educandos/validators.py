import re

from django.core.exceptions import ValidationError


def somente_digitos(valor: str) -> str:
    return re.sub(r"\D", "", valor or "")


def normalizar_cpf(valor: str) -> str:
    return somente_digitos(valor)


def validar_cpf(valor: str) -> None:
    cpf = normalizar_cpf(valor)

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        raise ValidationError("Informe um CPF válido com 11 dígitos.")

    for tamanho in (9, 10):
        soma = sum(int(cpf[indice]) * (tamanho + 1 - indice) for indice in range(tamanho))
        digito = (soma * 10) % 11
        if digito == 10:
            digito = 0
        if digito != int(cpf[tamanho]):
            raise ValidationError("Informe um CPF válido.")


def validar_contato(valor: str) -> None:
    digitos = somente_digitos(valor)
    if len(digitos) not in (10, 11):
        raise ValidationError("Informe um telefone com DDD e 10 ou 11 dígitos.")
