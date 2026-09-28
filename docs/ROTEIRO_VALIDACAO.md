# Roteiro de validação da Sprint 1

Antes da demonstração:

```cmd
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py test
```

## T-01 — RF01 com dados válidos

1. Entre com usuário autorizado.
2. Abra **Educandos → Novo educando**.
3. Informe dados totalmente fictícios e salve.
4. Confirme que o registro aparece na lista após nova consulta.

Resultado: cadastro aceito e persistido.

## T-02 — RF01 com dados inválidos

Repita o cadastro com campo obrigatório vazio, CPF inválido, CPF duplicado e nascimento futuro.

Resultado: cadastro bloqueado e campo identificado; nenhum registro parcial.

## T-03 — RF02 com dois responsáveis

Cadastre um núcleo e preencha os dois formulários de responsáveis.

Resultado: núcleo e dois responsáveis aparecem juntos na consulta. Se qualquer formulário for inválido, nada deve ser persistido.

## T-04 — RF03 repetindo vínculo

Crie um vínculo válido e tente cadastrar novamente a mesma combinação.

Resultado: duplicidade bloqueada e apenas um vínculo mantido.

## T-05 — RF04 sem permissão

Utilize um usuário sem a permissão de adicionar situação socioassistencial e tente acessar a rota.

Resultado: acesso HTTP 403 e nenhum dado persistido.

## T-06 — RF30 com dados

Abra o relatório com um filtro que alcance a massa fictícia.

Resultado: apenas o recorte selecionado e os quatro indicadores documentados.

## T-07 — RF30 sem dados e filtro inválido

Pesquise um nome inexistente e depois informe data inicial posterior à final.

Resultado: estado vazio claro no primeiro caso e mensagem de validação no segundo, sem erro de aplicação.

Capturas de tela nunca devem conter dados reais de pessoas atendidas.
