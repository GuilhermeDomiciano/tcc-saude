# Backend Architecture Guide

Visão geral
- Organização por camadas para facilitar testes e evolução incremental.
- Modo Dev (SQLite) com seed automático; modo Prod (Postgres) com Alembic e criação de schemas `dw`/`stage` no startup.
- Escrita protegida por `X-API-Key` se `API_KEY` estiver definido no ambiente.

Pastas
- `app/core`: configuração (env, CORS, erros, segurança) e integração com DB (`engine`, `get_session`).
- `app/api`: camada HTTP (FastAPI) e roteadores.
- `app/api/routes`: módulos de rotas por domínio (`territorios`, `tempo`, `unidades`, `equipes`, `fontes`, `pop_faixa`, `fatos`).
- `app/models`: entidades ORM (SQLModel). `dw.py` (prod) e `dev_lite.py` (SQLite-dev).
- `app/schemas`: DTOs Pydantic (Create/Update/Out) por dimensão.
- `app/services`: regras de negócio e orquestração de repositórios.
- `app/repositories`: consultas/persistência, validações de unicidade.
- `app/utils` e `app/workers`: utilitários e tarefas assíncronas (a definir).

Fluxo recomendado
1) Schemas (DTOs) em `app/schemas/<dominio>.py`.
2) Repositório em `app/repositories/<dominio>_repo.py` (list/get/create/update/delete).
3) Serviço em `app/services/<dominio>_service.py` (validações e conversões DTO↔modelo).
4) Rota em `app/api/routes/<dominio>.py` (handlers finos; dependências/segurança).

Execução
- Dev: `uvicorn main:app --reload --port 8000`.
- Prod/Postgres: defina `DATABASE_URL`, a API cria `dw`/`stage` e roda `alembic upgrade head` automaticamente.

Testes
- `pytest -q` (usa SQLite `dev_test.db` por padrão; sem API key).

Exemplo rápido (CRUD Territórios)
- Schemas: `app/schemas/territorio.py`
- Repo: `app/repositories/territorio_repo.py`
- Service: `app/services/territorio_service.py`
- Rotas: `app/api/routes/territorios.py`
