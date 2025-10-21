# Backend – MVP API

API FastAPI para cadastro e consulta das dimensões analíticas (tempo, território, população por faixa/sexo, unidade, equipe e fonte de recurso). Suporta modo Dev (SQLite) e Prod (Postgres/Supabase com Alembic).

## Requisitos
- Python 3.11+
- `pip install -r backend/requirements.txt`

## Ambiente
- Copie e ajuste o `.env` na raiz (exemplo padrão Dev):
  - `DATABASE_URL=sqlite:///./dev.db`
  - `ALLOWED_ORIGINS=http://localhost:5173`
  - (Opcional) `API_KEY=...` para exigir `X-API-Key` nos métodos de escrita

## Executar (Dev)
- `cd backend`
- `uvicorn main:app --reload --port 8000`
- Health: `GET http://localhost:8000/health`

## Executar (Prod – Postgres/Supabase)
- Defina `DATABASE_URL=postgresql+psycopg://USER:PASS@HOST:5432/DB?sslmode=require`
- A API garante os schemas `dw`/`stage` e executa `alembic upgrade head` no startup.
- Alternativa manual: `cd backend && alembic upgrade head`

## Segurança
- Escrita exige header `X-API-Key` se `API_KEY` estiver definido no ambiente.
- Leitura (GET) é livre por padrão no MVP.

## Endpoints principais
- Saúde
  - `GET /health` – status básico
- Dimensões (CRUD)
  - `GET/POST/PUT/DELETE /dw/territorios`
  - `GET/POST/PUT/DELETE /dw/tempo` (filtros: `ano`, `mes`)
  - `GET/POST/PUT/DELETE /dw/pop-faixa` (filtros: `territorio_id`, `ano`)
  - `GET/POST/PUT/DELETE /dw/unidades`
  - `GET/POST/PUT/DELETE /dw/equipes`
  - `GET/POST/PUT/DELETE /dw/fontes`
- Fatos (leitura)
  - `GET /dw/fatos/cobertura` (filtros: `data_ini`, `data_fim`, `territorio_id`)

## Exemplos (curl)
- Criar território (com API key):
```
curl -X POST http://localhost:8000/dw/territorios \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "cod_ibge_municipio":"4300000",
    "nome":"Municipio A",
    "uf":"RS",
    "area_km2":123.45
  }'
```
- Listar tempo (filtrado):
```
curl "http://localhost:8000/dw/tempo?ano=2025&mes=1"
```

## Testes
- `cd backend && pytest -q`

## Migrações (Alembic)
- Configuração: `backend/alembic.ini`, scripts em `backend/alembic/versions/`
- Rodar: `cd backend && alembic upgrade head`
- Gerar nova migração (quando necessário):
  - `alembic revision -m "sua_mudanca" --autogenerate`


## RDQA � Endpoints e Exemplos

- GET /public/verificar?exec_id=...&hash=... � Verifica��o p�blica de artefatos.
  - Ex.: curl "http://localhost:8000/public/verificar?exec_id=UUID&hash=HASH"

- GET /rdqa/consistencia?periodo=2025-01 � Lista indicadores com MAPE.
- GET /rdqa/consistencia/{indicador}/detalhes?periodo=2025-01 � Drill-down por indicador.
- GET /rdqa/cobertura?periodo=2025-01 � Cobertura de quadros gerados.
- GET /rdqa/diff?periodo_atual=2025-02&periodo_anterior=2025-01&indicadores=cov_aps � Diferen�as entre per�odos.

- POST /rdqa/export/pdf � Gera PDF a partir de HTML/URL.
  - Body: { "html": "<html>...</html>", "format": "A4", "margin_mm": 12 }
  - Headers de resposta: X-Exec-Id, X-Hash.

- POST /rdqa/export/pacote � Gera pacote ZIP de reprodutibilidade.
  - Headers de resposta: X-Exec-Id, X-Hash.
  - Ex.: curl -X POST -H "X-API-Key: " -o rdqa.zip http://localhost:8000/rdqa/export/pacote

Notas:
- Quando API_KEY estiver definida, os endpoints de gera��o (/rdqa/export/*) exigem o header X-API-Key.
- O frontend usa X-Exec-Id/X-Hash para montar QR Code e verifica��o p�blica.


