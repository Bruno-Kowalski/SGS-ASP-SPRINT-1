# SGS-ASP — Sprint 1

Implementação local da primeira sprint do Sistema de Gestão Socioassistencial da Associação Ação Social do Planalto.

## Escopo implementado

- RF01 — cadastro das informações pessoais do educando;
- RF02 — cadastro do núcleo familiar e de seus responsáveis;
- RF03 — vínculo entre educando e responsável existente;
- RF04 — registro da situação socioassistencial;
- RF30 — relatório de acompanhamento com dados e indicadores disponíveis na Sprint 1.

O projeto não implementa requisitos das próximas sprints. Autenticação customizada, perfis institucionais, atividades, frequência, atendimentos, anexos e doações permanecem fora deste incremento. Para proteger RF04 e RF30, a Sprint 1 utiliza provisoriamente o sistema nativo de usuários e permissões do Django.

## Tecnologias

- Python 3.13;
- Django 5.2 LTS;
- PostgreSQL 17;
- Django Templates;
- Django ORM.

## 1. Preparar o projeto no Windows

Abra a pasta no VS Code e, no terminal, execute:

```cmd
py -3.13 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Se estiver usando PowerShell, a ativação é:

```powershell
& .\.venv\Scripts\Activate.ps1
```

## 2. Criar o banco PostgreSQL

Entre no `psql` com o usuário administrador:

```cmd
psql -U postgres
```

Execute:

```sql
CREATE USER sgs_asp WITH PASSWORD 'defina-uma-senha-local';
CREATE DATABASE sgs_asp OWNER sgs_asp ENCODING 'UTF8';
\q
```

## 3. Configurar as variáveis

Copie o exemplo:

```cmd
copy .env.example .env
```

Abra `.env` e ajuste pelo menos:

```env
DJANGO_SECRET_KEY=uma-chave-local-diferente-e-segura
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_USE_SQLITE=False
POSTGRES_DB=sgs_asp
POSTGRES_USER=sgs_asp
POSTGRES_PASSWORD=defina-uma-senha-local
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

O arquivo `.env` está no `.gitignore` e não deve ser enviado ao GitHub.

## 4. Criar as tabelas

```cmd
python manage.py check
python manage.py migrate
python manage.py makemigrations --check --dry-run
```

O último comando deve responder `No changes detected`.

## 5. Criar o usuário local

```cmd
python manage.py createsuperuser
```

O superusuário possui todas as permissões necessárias para validar a Sprint 1. A interface própria de gestão de usuários pertence à Sprint 2 e não foi antecipada.

## 6. Executar

```cmd
python manage.py runserver
```

Acesse:

- aplicação: http://127.0.0.1:8000/
- administração: http://127.0.0.1:8000/admin/

Entre primeiro na administração com o superusuário e depois acesse a aplicação.

## 7. Executar os testes

### Teste rápido sem PostgreSQL

No Prompt de Comando:

```cmd
set DJANGO_USE_SQLITE=True
python manage.py test
set DJANGO_USE_SQLITE=
```

No PowerShell:

```powershell
$env:DJANGO_USE_SQLITE="True"
python manage.py test
Remove-Item Env:DJANGO_USE_SQLITE
```

### Teste final com PostgreSQL

Mantenha `DJANGO_USE_SQLITE=False` no `.env` e execute:

```cmd
python manage.py test
```

O usuário PostgreSQL precisará de permissão para criar o banco temporário de testes. A validação final da entrega deve ser feita no PostgreSQL.

## Ordem recomendada da demonstração

1. RF01: cadastrar um educando com dados fictícios;
2. RF02: cadastrar um núcleo e ao menos um responsável fictício;
3. RF03: vincular o educando ao responsável;
4. RF04: registrar uma situação socioassistencial fictícia;
5. RF30: abrir o relatório, aplicar filtros e conferir os indicadores.

Consulte também:

- `docs/MAPEAMENTO_ISSUES.md`;
- `docs/RF30_INDICADORES.md`;
- `docs/ROTEIRO_VALIDACAO.md`;
- `docs/GUIA_ARQUIVOS.md`.
