# Repository Guidelines

## Project Structure & Module Organization
- `backend/`: API FastAPI + SQLModel. Entrada em `backend/main.py`.
- `backend/app/`: código por camadas — `core/`, `api/`, `models/`, `schemas/`, `services/`, `repositories/`, `utils/`, `workers/`.
- `backend/alembic/`: migrações (DW + stage) e config `alembic.ini`.
- `backend/tests/`: testes de API (pytest) `test_*.py`.
- `backend/db/`: arquivos SQL de contexto (não executar).

## Build, Test, and Development
- Dev: `cd backend && pip install -r requirements.txt && uvicorn main:app --reload --port 8000`
- Testes: `cd backend && pytest -q`
- Migração (Postgres): `cd backend && set DATABASE_URL=... && alembic upgrade head`

## Coding Style & Naming
- Python: PEP 8, indentação 4 espaços, type hints. DTOs em `app/schemas`, models ORM em `app/models`, regra em `app/services` e acesso a dados em `app/repositories`.
- Handlers finos nas rotas; delegar a services.

## Testing Guidelines
- Escreva testes em `backend/tests/` com `TestClient`. Use fixtures em `conftest.py`.
- Foque em CRUD das dimensões e validações (UF, IBGE, datas) e filtros.

## Commit & Pull Request Guidelines
- Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`.
- PRs: descrição clara, passos de validação e resultados (logs/tests).

## Security & Config Tips
- Env no `.env` da raiz: `DATABASE_URL` (dev: `sqlite:///./dev.db`), `ALLOWED_ORIGINS`, e opcional `API_KEY` (exige header `X-API-Key` para escrita).
- Em Postgres: a API cria `dw`/`stage` e executa Alembic no startup.
