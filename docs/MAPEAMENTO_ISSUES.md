# Mapeamento das issues e sub-issues da Sprint 1

## RF01 — Issue #2

| Sub-issue | Implementação |
|---|---|
| #58 — Modelar o educando e criar formulário, view e template | `Educando`, `EducandoForm`, `EducandoCreateView` e templates de cadastro/listagem. |
| #59 — Validações, migration e PostgreSQL | CPF válido e único, obrigatórios, nascimento não futuro, migration `0001_initial.py` e Django ORM. |
| #60 — Testes e evidências | Testes de cadastro válido, campos vazios, CPF inválido/duplicado, data futura, permissão e persistência. |

## RF02 — Issue #3

| Sub-issue | Implementação |
|---|---|
| #61 — Modelar núcleo e formulário | `NucleoFamiliar`, formulário e tela de cadastro. |
| #62 — Incluir e organizar responsáveis e membros | `Responsavel` e formset com um ou mais responsáveis. |
| #63 — Vínculos, constraints e persistência | FK responsável–núcleo, identificação e CPF únicos e serviço transacional. |
| #64 — Testar fluxo e registrar evidências | Testes com dois responsáveis e teste que comprova que dados inválidos não persistem o núcleo. |

## RF03 — Issue #4

| Sub-issue | Implementação |
|---|---|
| #68 — Selecionar educando e responsável existentes | `VinculoEducandoResponsavelForm` consulta registros persistidos. |
| #69 — Criar vínculo e bloquear combinações inválidas/duplicadas | Serviço transacional, validação de núcleo e constraints de unicidade. |
| #70 — Testar vínculo e registrar evidências | Testes de vínculo válido, núcleos diferentes e repetição do vínculo. |

## RF04 — Issue #5

| Sub-issue | Implementação |
|---|---|
| #65 — Modelar e criar formulário | `SituacaoSocioassistencial`, formulário e telas. |
| #66 — Validar, vincular e persistir | FK para educando, campos obrigatórios, data não futura, usuário responsável e permissão Django. |
| #67 — Testes e evidências fictícias | Testes de data, acesso negado, persistência autorizada e rastreabilidade do usuário. |

## RF30 — Issue #31

| Sub-issue | Implementação |
|---|---|
| #71 — Definir dados, filtros e indicadores | Especificação em `RF30_INDICADORES.md` e `RelatorioDesenvolvimentoFiltroForm`. |
| #72 — Consultas no Django ORM | `selectors.py`, com `select_related`, `prefetch_related`, filtros e consultas agregadas. |
| #73 — Visualização em template | `templates/relatorios/desenvolvimento.html`. |
| #74 — Testar filtros, resultados e permissões | Testes de acesso negado, indicadores, nome, resultado vazio e período inválido. |

As referências numéricas documentam a rastreabilidade. Nenhum commit, issue ou pull request foi criado ou alterado automaticamente.
