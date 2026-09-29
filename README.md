# SGS-ASP — Sprint 1

Implementação da primeira sprint do **Sistema de Gestão Socioassistencial da Associação Ação Social do Planalto (SGS-ASP)**.

O sistema foi desenvolvido com Python e Django. Neste primeiro momento, o banco de dados utilizado para desenvolvimento e testes locais é o **SQLite**. A migração e a validação com PostgreSQL serão realizadas posteriormente.

## Escopo implementado

- **RF01** — cadastro das informações pessoais do educando;
- **RF02** — cadastro do núcleo familiar e de seus responsáveis;
- **RF03** — vínculo entre educando e responsável existente;
- **RF04** — registro da situação socioassistencial;
- **RF30** — relatório de acompanhamento com os dados e indicadores disponíveis na Sprint 1.

O projeto não implementa requisitos das próximas sprints. Autenticação customizada, perfis institucionais, atividades, frequência, atendimentos, anexos e doações permanecem fora deste incremento.

Para proteger as funcionalidades restritas durante a Sprint 1, o sistema utiliza provisoriamente a autenticação e as permissões nativas do Django.

## Tecnologias utilizadas

- Python 3.13;
- Django 5.2 LTS;
- SQLite para desenvolvimento e testes iniciais;
- Django Templates;
- Django ORM;
- HTML e CSS.

## Pré-requisitos

Antes de começar, instale no computador:

- [Git](https://git-scm.com/downloads);
- [Python 3.13](https://www.python.org/downloads/);
- Visual Studio Code ou outro editor de código;
- conexão com a internet para clonar o repositório e instalar as dependências.

Durante a instalação do Python no Windows, marque a opção **Add Python to PATH**.

Os comandos deste guia foram preparados para o **Prompt de Comando do Windows (CMD)**.

## 1. Clonar o repositório

Abra o Prompt de Comando ou o terminal do VS Code e escolha a pasta onde o projeto será armazenado. Exemplo:

```cmd
cd %USERPROFILE%\Downloads
```

Clone o repositório:

```cmd
git clone https://github.com/Bruno-Kowalski/SGS-ASP-SPRINT-1.git
```

Entre na pasta criada:

```cmd
cd SGS-ASP-SPRINT-1
```

Como o repositório é privado, o GitHub poderá solicitar autenticação.

Confirme que está na pasta correta:

```cmd
dir
```

Entre os arquivos exibidos devem estar:

```text
manage.py
requirements.txt
.env.example
apps
config
templates
```

## 2. Verificar o Python

Execute:

```cmd
python --version
```

O resultado esperado é semelhante a:

```text
Python 3.13.x
```

Caso o comando não seja reconhecido, verifique a instalação:

```cmd
where python
```

## 3. Criar o ambiente virtual

Na raiz do projeto, execute:

```cmd
python -m venv .venv
```

Ative o ambiente virtual:

```cmd
.venv\Scripts\activate.bat
```

Após a ativação, o início do terminal deverá mostrar `(.venv)`:

```text
(.venv) C:\Users\seu-usuario\Downloads\SGS-ASP-SPRINT-1>
```

> Não abra o arquivo `Activate.ps1` com duplo clique. A ativação deve ser executada como comando no terminal.

Se estiver utilizando PowerShell, use:

```powershell
& .\.venv\Scripts\Activate.ps1
```

## 4. Instalar as dependências

Com o ambiente virtual ativado, atualize o `pip`:

```cmd
python -m pip install --upgrade pip
```

Instale as dependências do projeto:

```cmd
python -m pip install -r requirements.txt
```

Confirme a instalação do Django:

```cmd
python -m django --version
```

O resultado esperado é uma versão `5.2.x`.

## 5. Configurar o SQLite

Crie o arquivo local de configuração a partir do exemplo:

```cmd
copy .env.example .env
```

Abra o arquivo:

```cmd
notepad .env
```

Deixe a configuração desta forma:

```env
DJANGO_SECRET_KEY=troque-por-uma-chave-local
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_USE_SQLITE=True
```

As variáveis do PostgreSQL existentes no final do arquivo podem permanecer. Elas serão ignoradas enquanto `DJANGO_USE_SQLITE=True`.

O arquivo `.env` contém configurações locais, está protegido pelo `.gitignore` e não deve ser enviado ao GitHub.

## 6. Verificar o projeto

Execute a verificação do Django:

```cmd
python manage.py check
```

Resultado esperado:

```text
System check identified no issues (0 silenced).
```

Verifique também se não existem migrations pendentes:

```cmd
python manage.py makemigrations --check --dry-run
```

Resultado esperado:

```text
No changes detected
```

## 7. Criar o banco de dados

Execute as migrations:

```cmd
python manage.py migrate
```

O Django criará automaticamente o arquivo `db.sqlite3` na raiz do projeto. Esse arquivo representa o banco local e não deve ser enviado ao GitHub.

## 8. Executar os testes automatizados

Execute:

```cmd
python manage.py test
```

Todos os testes devem terminar com `OK`. A quantidade pode aumentar conforme o projeto evoluir. Na versão inicial da Sprint 1, o resultado esperado é semelhante a:

```text
Ran 22 tests

OK
```

## 9. Criar um usuário administrador

Para acessar as funcionalidades protegidas, crie um superusuário local:

```cmd
python manage.py createsuperuser
```

O terminal solicitará:

- nome de usuário;
- e-mail, que pode ser deixado em branco;
- senha;
- confirmação da senha.

Enquanto a senha é digitada, nenhum caractere aparece no terminal. Esse comportamento é normal.

O usuário criado existe somente no banco SQLite local.

## 10. Iniciar a aplicação

Execute:

```cmd
python manage.py runserver
```

Acesse no navegador:

- aplicação: <http://127.0.0.1:8000/>;
- administração do Django: <http://127.0.0.1:8000/admin/>.

Entre com o superusuário criado anteriormente. Para interromper a aplicação, volte ao terminal e pressione `Ctrl + C`.

## 11. Ordem recomendada para testar a Sprint 1

Utilize somente informações fictícias durante os testes.

1. Cadastre um núcleo familiar e seus dados básicos — RF02.
2. Cadastre um responsável dentro do núcleo familiar — RF02.
3. Cadastre um educando com informações pessoais — RF01.
4. Vincule o educando ao responsável existente — RF03.
5. Registre a situação socioassistencial do educando — RF04.
6. Abra o relatório de desenvolvimento — RF30.
7. Aplique os filtros e confira os indicadores apresentados.
8. Teste campos obrigatórios, dados inválidos e vínculos duplicados.

Não utilize nomes, CPFs, telefones, endereços ou outras informações pessoais reais.

## 12. Executar novamente em outro momento

Depois da primeira configuração, não é necessário recriar o ambiente virtual nem reinstalar as dependências a cada execução.

Abra o terminal, entre na pasta do projeto e execute:

```cmd
cd %USERPROFILE%\Downloads\SGS-ASP-SPRINT-1
.venv\Scripts\activate.bat
python manage.py runserver
```

Ao terminar, pressione `Ctrl + C` e, se desejar sair do ambiente virtual, execute:

```cmd
deactivate
```

## Comandos de validação da entrega

Antes de considerar o incremento concluído, execute:

```cmd
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Os três comandos devem concluir sem erros.

## Problemas comuns

### `No suitable Python runtime found`

O inicializador `py` não encontrou a versão solicitada. Utilize o executável disponível diretamente:

```cmd
python --version
python -m venv .venv
```

### `python` não é reconhecido

O Python não está instalado corretamente ou não foi adicionado ao `PATH`. Reinstale o Python e marque **Add Python to PATH**.

### `No module named django`

Ative o ambiente virtual e instale novamente as dependências:

```cmd
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

### `python: can't open file 'manage.py'`

O terminal está na pasta errada. Entre na pasta que contém o arquivo `manage.py`:

```cmd
cd %USERPROFILE%\Downloads\SGS-ASP-SPRINT-1
```

### Erro relacionado ao PostgreSQL

Confirme no arquivo `.env` que o SQLite está habilitado:

```env
DJANGO_USE_SQLITE=True
```

Como alternativa temporária no CMD:

```cmd
set DJANGO_USE_SQLITE=True
```

### Tabela inexistente

Execute novamente as migrations:

```cmd
python manage.py migrate
```

### Porta 8000 ocupada

Inicie a aplicação em outra porta:

```cmd
python manage.py runserver 8001
```

Depois, acesse <http://127.0.0.1:8001/>.

## Arquivos que não devem ser enviados ao GitHub

O `.gitignore` do projeto já exclui, entre outros:

```text
.venv/
.env
db.sqlite3
__pycache__/
.vscode/
.idea/
```

Antes de criar um commit, confira:

```cmd
git status
```

Garanta que `.env`, `.venv` e `db.sqlite3` não estejam na lista de arquivos preparados para envio.

## Estrutura principal

```text
SGS-ASP-SPRINT-1/
├── manage.py
├── requirements.txt
├── config/
├── apps/
│   ├── educandos/
│   └── relatorios/
├── templates/
├── static/
└── docs/
```

- `config`: configurações gerais, URLs e inicialização do Django;
- `apps/educandos`: implementação dos requisitos RF01, RF02, RF03 e RF04;
- `apps/relatorios`: implementação do RF30;
- `templates`: páginas HTML;
- `static`: estilos CSS;
- `docs`: documentação técnica, mapeamento das issues e roteiro de validação.

## Migração futura para PostgreSQL

O PostgreSQL continua sendo o banco oficial planejado para o SGS-ASP. O SQLite está sendo utilizado temporariamente para facilitar o desenvolvimento e os testes iniciais.

Os dados cadastrados no SQLite não serão transferidos automaticamente para o PostgreSQL. Por isso, mantenha somente dados fictícios no banco atual. Quando a migração for realizada, as mesmas migrations do Django serão aplicadas em um banco PostgreSQL limpo.

## Documentação complementar

- [`docs/MAPEAMENTO_ISSUES.md`](docs/MAPEAMENTO_ISSUES.md);
- [`docs/RF30_INDICADORES.md`](docs/RF30_INDICADORES.md);
- [`docs/ROTEIRO_VALIDACAO.md`](docs/ROTEIRO_VALIDACAO.md);
- [`docs/GUIA_ARQUIVOS.md`](docs/GUIA_ARQUIVOS.md);
- [`docs/SUGESTAO_COMMITS.md`](docs/SUGESTAO_COMMITS.md).
