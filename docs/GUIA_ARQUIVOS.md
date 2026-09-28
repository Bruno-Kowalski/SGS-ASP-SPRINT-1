# Guia dos arquivos

## Configuração

- `manage.py`: executa os comandos do Django.
- `config/settings.py`: configura aplicações, PostgreSQL, idioma, horário, templates e segurança básica.
- `config/urls.py`: distribui as URLs para os módulos.
- `.env.example`: modelo das variáveis locais; a senha real fica no `.env` ignorado pelo Git.
- `requirements.txt`: fixa as dependências utilizadas.

## Aplicação `educandos`

- `models.py`: tabelas e constraints de RF01–RF04.
- `validators.py`: valida CPF e telefone.
- `forms.py`: recebe e valida os campos enviados pelas telas.
- `services.py`: executa operações que precisam de transação, como núcleo com responsáveis e vínculo.
- `views.py`: controla as requisições, permissões, mensagens e respostas.
- `urls.py`: nomes e endereços das telas.
- `admin.py`: disponibiliza os modelos no painel administrativo.
- `migrations/0001_initial.py`: versão inicial da estrutura do banco.
- `tests/`: testes automatizados dos models, forms, services, views e permissões.

## Aplicação `relatorios`

- `forms.py`: filtros do RF30.
- `selectors.py`: consultas de leitura no Django ORM e cálculo dos indicadores.
- `views.py`: verifica a permissão e envia o resultado ao template.
- `urls.py`: endereço do relatório.
- `tests/`: valida acesso, filtros, indicadores e estado vazio.

Não existe tabela própria para relatório. Ele é derivado dos dados já persistidos, conforme a modelagem do produto.

## Interface

- `templates/base.html`: estrutura comum e menu.
- `templates/inicio.html`: painel inicial.
- `templates/educandos/`: formulários e listas de RF01–RF04.
- `templates/relatorios/desenvolvimento.html`: tela do RF30.
- `static/css/sistema.css`: layout responsivo e identidade visual.
