# Plano de Implementação do MVP (Backend)

Objetivo: disponibilizar cadastro (CRUD) e consulta dos dados de referência usados como parâmetros analíticos: tempo, território (IBGE), população por faixa etária/sexo, unidade (CNES), equipe (APS) e fonte de recurso. Esses dados alimentam cálculos posteriores (fatos/relatórios).

## 1) Fundações e Ambiente
- [x] Definir `DATABASE_URL` (dev: SQLite; prod: Postgres/Supabase).
  - Use `backend/.env.example` como base (`DATABASE_URL=sqlite:///./dev.db`).
- [x] Confirmar CORS `ALLOWED_ORIGINS`.
  - Ajuste no `.env` (ex.: `http://localhost:5173`).
- [x] Instalar deps: `pip install -r backend/requirements.txt`.
  - Inclui `python-dotenv` para carregar `.env` automaticamente.
- [ ] (Opcional prod) Configurar Alembic para migrações.

## 2) Modelos e Migrações (DW + Stage)
- [x] Modelos DW e Stage prontos em `app/models/dw.py` e `app/models/stage.py`.
- [x] Criar migração inicial (Alembic) com schemas `dw` e `stage` e todas as tabelas necessárias.
  - Arquivos: `backend/alembic.ini`, `backend/alembic/env.py`, `backend/alembic/versions/0001_init_dw_stage.py`.
  - Rodar (Postgres): `cd backend && set DATABASE_URL=postgresql+psycopg://... && alembic upgrade head`.
  - Observação: a migração cria schemas apenas em Postgres; para SQLite-dev, usar o seed do app.
- [ ] (Opcional) Criar views utilitárias (`vw_denominador_populacao`, `vw_dim_tempo_flags`, `vw_financas_execucao`).

## 3) Conexão e Sessão (DB)
- [x] Engine e sessão em `app/core/db.py` (SQLite-dev; Postgres-prod).
- [x] Startup (prod): `alembic upgrade head` e criação dos schemas `dw`/`stage` caso ausentes.
  - Implementado em `backend/main.py` (detecta Postgres e roda Alembic automaticamente).

## 4) Schemas (DTOs)
- [x] DTOs iniciais: território/tempo em `app/schemas/*`.
- [x] Adicionar DTOs Create/Update/Out para:
  - [x] `DimTerritorio` (Create/Update/Out)
  - [x] `DimTempo` (Create/Update/Out)
  - [x] `DimPopFaixaEtaria` (Create/Update/Out)
  - [x] `DimUnidade` (Create/Update/Out)
  - [x] `DimEquipe` (Create/Update/Out)
  - [x] `DimFonteRecurso` (Create/Update/Out)

## 5) Repositórios
- [x] Repositório básico de território/tempo.
- [x] Implementar CRUD repositório para cada dimensão acima (list/get/create/update/delete) com validações simples (ex.: chaves únicas).
  - Território: `app/repositories/territorio_repo.py`
  - Tempo: `app/repositories/tempo_repo.py`
  - Pop Faixa Etária: `app/repositories/pop_faixa_repo.py`
  - Unidade: `app/repositories/unidade_repo.py`
  - Equipe: `app/repositories/equipe_repo.py`
  - Fonte Recurso: `app/repositories/fonte_repo.py`

## 6) Serviços (Regras)
- [x] Serviços de listagem iniciais.
- [ ] Encapsular regras de negócio (ex.: validação de UF, formato IBGE, faixas etárias válidas).

## 7) Rotas (API)
- [x] GET saúde: `/health`.
- [x] GET listas: `/dw/territorios`, `/dw/unidades`, `/dw/tempo`, `/dw/fatos/cobertura`.
- [ ] Implementar CRUD das dimensões:
  - [ ] Território: `GET/POST/PUT/DELETE /dw/territorios`
  - [ ] Tempo: `GET/POST/PUT/DELETE /dw/tempo`
  - [ ] População Faixa Etária: `GET/POST/PUT/DELETE /dw/pop-faixa`
  - [ ] Unidade: `GET/POST/PUT/DELETE /dw/unidades`
  - [ ] Equipe: `GET/POST/PUT/DELETE /dw/equipes`
  - [ ] Fonte Recurso: `GET/POST/PUT/DELETE /dw/fontes`
- [ ] Paginação padrão (`limit/offset`), filtros por campos chave (UF, ano/mes, etc.).

## 8) Qualidade e Segurança
- [ ] Tratamento de erros padronizado (HTTPException mensagens claras).
- [ ] (Opcional MVP) Chave de API simples para métodos de escrita.
- [ ] OpenAPI tags e exemplos nos endpoints.

## 9) Dados de Exemplo (Dev)
- [x] Seed dev para SQLite em `main.py` (território/unidade/tempo).
- [ ] Acrescentar seed leve para `dim_pop_faixa_etaria`.

## 10) Testes
- [ ] Testes unitários de serviços/repositórios (SQLite em memória).
- [ ] Testes de API com `TestClient` (FastAPI).

## 11) Entrega
- [ ] Documentar rotas e exemplos no README do backend.
- [ ] Preparar `alembic.ini`/pipelines para deploy (prod: Postgres/Supabase).
