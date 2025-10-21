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
- [x] Encapsular regras de negócio (ex.: validação de UF, formato IBGE, faixas etárias válidas).
  - Território: valida UF (uppercase, 2 chars) e IBGE (6–7 dígitos); CRUD em `app/services/territorio_service.py`.
  - Tempo: parse de data ISO (YYYY-MM-DD); CRUD em `app/services/tempo_service.py`.
  - Unidade: trims/validação simples; CRUD em `app/services/unidade_service.py`.
  - Equipe: tipo válido (ESF/ESB/ACS/OUTROS); CRUD em `app/services/equipe_service.py`.
  - Fonte: código único; CRUD em `app/services/fonte_service.py`.
  - Pop Faixa: chave composta única; CRUD em `app/services/pop_faixa_service.py`.

## 7) Rotas (API)
- [x] GET saúde: `/health`.
- [x] GET listas: `/dw/territorios`, `/dw/unidades`, `/dw/tempo`, `/dw/fatos/cobertura`.
- [x] Implementar CRUD das dimensões:
  - [x] Território: `GET/POST/PUT/DELETE /dw/territorios`
  - [x] Tempo: `GET/POST/PUT/DELETE /dw/tempo`
  - [x] População Faixa Etária: `GET/POST/PUT/DELETE /dw/pop-faixa`
  - [x] Unidade: `GET/POST/PUT/DELETE /dw/unidades`
  - [x] Equipe: `GET/POST/PUT/DELETE /dw/equipes`
  - [x] Fonte Recurso: `GET/POST/PUT/DELETE /dw/fontes`
- [x] Paginação padrão (`limit/offset`) e filtros iniciais (ano/mes, territorio_id).

## 8) Qualidade e Segurança
- [x] Tratamento de erros padronizado: `app/core/errors.py` (ValueError→400, IntegrityError→409).
- [x] Chave de API simples para escrita: header `X-API-Key` (habilita se `API_KEY` definido no ambiente).
- [x] OpenAPI: exemplos adicionados nos DTOs de criação (tempo/território). Tags já configuradas por rota.

## 9) Dados de Exemplo (Dev)
- [x] Seed dev para SQLite em `main.py` (território/unidade/tempo).
- [x] Acrescentar seed leve para `dim_pop_faixa_etaria` (versão dev `DevDimPopFaixaEtaria`).

## 10) Testes
- [x] Testes de API com `TestClient` (FastAPI) em `backend/tests/`.
  - `test_health.py`, `test_territorios.py`, `test_tempo.py`, `test_unidades.py`.
  - Execução: `cd backend && pytest -q`.
- [ ] (Opcional) Testes unitários de serviços/repositórios (SQLite em memória).

## 11) Entrega
- [x] Documentar rotas e exemplos no README do backend (`backend/README.md`).
- [x] Preparar `alembic.ini`/migrations para deploy (prod: Postgres/Supabase).
  - Startup em Postgres cria schemas e roda `alembic upgrade head` automaticamente.

-## 12) Alinhamento adicional com o Frontend/JIC
- [x] DTOs `Out` com Proveniência: adicionar campos opcionais `fonte`, `periodo`, `versao` (e, quando houver, `hash`, `exec_id`) nas respostas das dimensões.
- [x] Filtros adicionais nas listas:
  - Territórios: `uf`, `cod_ibge_municipio`.
  - Unidades: `cnes`, `territorio_id` (além de `uf`, se aplicável).
  - Equipes: `tipo` (ESF/ESB/ACS/OUTROS), `ativo` (bool).
  - Fontes: `codigo`.
  - Manter `limit/offset` em todas.
- [ ] Exportação RDQA (PDF): endpoint `POST /rdqa/export/pdf` (WeasyPrint/Pyppeteer) com retorno `application/pdf`; registrar `exec_id/hash` para QR. (stub criado)
- [x] Verificação pública (QR): endpoint `GET /public/verificar?exec_id=...&hash=...` retornando metadados/estado do artefato. (stub)
- [ ] OpenAPI: documentar novos filtros e campos de proveniência; exemplos de uso do export/QR.
- [ ] Testes: cobrir filtros adicionados e fluxos do exportador/rota pública (mocks onde necessário).
