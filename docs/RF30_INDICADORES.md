# RF30 — Dados, filtros e indicadores da Sprint 1

## Limite do relatório

A documentação exige a definição dos dados e indicadores antes da conclusão do RF30, mas não fornece cálculos específicos. Para não antecipar atividades, frequência, atendimentos ou outros requisitos futuros, este incremento utiliza somente dados produzidos por RF01, RF02, RF03 e RF04.

O relatório deve ser descrito como relatório inicial de acompanhamento. Ele não representa ainda a evolução pedagógica completa do educando.

## Fontes

- `Educando`: identificação por nome e data de nascimento;
- `NucleoFamiliar`: núcleo ao qual o educando está vinculado;
- `VinculoEducandoResponsavel`: existência do vínculo com responsável;
- `SituacaoSocioassistencial`: situação mais recente dentro do recorte selecionado.

O CPF não é exibido no relatório para reduzir exposição de dado pessoal.

## Filtros

- educando específico;
- trecho do nome;
- data inicial da situação socioassistencial;
- data final da situação socioassistencial.

A data inicial não pode ser posterior à final. Quando o período é informado, entram no resultado apenas educandos que possuem situação socioassistencial no intervalo.

## Indicadores

| Indicador | Cálculo |
|---|---|
| Educandos no recorte | Quantidade de educandos após aplicação dos filtros. |
| Com núcleo familiar | Educandos do recorte com `nucleo_familiar` preenchido. |
| Com responsável | Educandos do recorte com ao menos um vínculo persistido. |
| Com situação registrada | Educandos do recorte com situação; quando existe período, a situação deve estar no intervalo. |

## Segurança

- acesso exige login;
- acesso exige a permissão `educandos.view_relatorio_desenvolvimento`;
- CPF não é exibido;
- testes e demonstrações devem utilizar somente dados fictícios.
