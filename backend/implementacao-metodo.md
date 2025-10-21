# Plano de Implementação do Método (Backend)

Objetivo: detalhar, em passos executáveis, as funcionalidades adicionais do método (rastreabilidade, consistência e reprodutibilidade) alinhadas ao artigo e ao frontend. Seguir a arquitetura do projeto: DTOs em `app/schemas`, modelos em `app/models`, regras em `app/services`, repositórios em `app/repositories` e rotas em `app/api/routes`. Exigir `X-API-Key` para escrita quando `API_KEY` estiver definido.

## 1) Verificação Pública Completa
- [x] Modelagem: criar entidade para registrar execuções e artefatos.
  - Opção: `dw.ArtefatoExecucao` com campos: `id (UUID)`, `hash_sha256`, `tipo` (ex.: `rdqa_pdf`), `fonte`, `periodo`, `versao`, `autor` (opcional), `created_at`, `metadados` (JSON resumido), `ok` (bool), `mensagem`.
  - Arquivos: `backend/app/models/dw.py` e migração em `backend/alembic/versions/*`.
- [ ] Schemas: DTOs para consulta pública e auditoria interna.
  - `app/schemas/artefato.py` – `ArtefatoExecucaoOut`, `ArtefatoExecucaoCheckIn`.
- [ ] Repositório: persistência e consulta por `exec_id`/`hash`.
  - `app/repositories/artefato_repo.py` com métodos `criar`, `obter_por_exec_id`, `verificar_por_hash`.
- [x] Serviço: orquestrar registro ao exportar e verificação pública.
  - `app/services/artefato_service.py` com `registrar_execucao(...)` e `verificar(exec_id, hash)`.
- [x] Rotas:
  - `GET /public/verificar?exec_id&hash`: retornar `ok`, metadados (fonte/periodo/versao), e mensagem clara.
    - Implementar em `backend/app/api/routes/public.py` (substituir o stub atual).
  - Integrar com exportação PDF: quando `POST /rdqa/export/pdf` gerar o PDF, registrar `exec_id/hash` no serviço e devolver nos headers `X-Exec-Id`/`X-Hash` (já existe o header; falta o registro).
- [x] Testes: cenários de verificação válida/ inválida/ parâmetros ausentes (pytest com `TestClient`).
  - `backend/tests/test_public_verificar_full.py`.

## 2) Quadro de Consistência (MAPE)
- [x] Fonte de referência: definir como armazenar valores esperados (planilha oficial) no `stage`.
  - Tabela exemplo: `stage.ref_indicadores` com colunas `indicador`, `chave` (dimensional), `valor_referencia`, `periodo`.
  - Migração Alembic correspondente.
- [x] Serviço de comparação: calcular MAPE por indicador.
  - `app/services/consistencia_service.py` com funções:
    - `listar_indicadores(periodo, filtros)` e `calcular_mape(indicador, periodo)`.
    - Opcional: `drill_down(indicador, periodo)` listando linhas divergentes (com `abs(erro)` ordenado).
- [x] Rotas API:
  - `GET /rdqa/consistencia?periodo&...` retorna: lista de indicadores com `mape`, valores atual vs referência e links para drill-down.
  - `GET /rdqa/consistencia/{indicador}/detalhes?periodo` para o drill-down.
- [x] Testes: MAPE com casos controlados (ex.: 0%, 3%, 10%).
  - `backend/tests/test_rdqa_consistencia.py`.

## 3) Cobertura RDQA
- [x] Modelagem (opcional, se necessário): tabela de controle de geração por quadro.
  - `dw.rdqa_quadro_execucao`: `quadro`, `periodo`, `territorio_id` (ou escopo), `status` (`gerado`/`faltando`), `motivo`, `created_at`.
- [x] Serviço: computar `%` de quadros gerados e listar faltantes com motivo.
  - `app/services/rdqa_cobertura_service.py` com `cobertura(periodo, filtros)`.
- [x] Rota API: `GET /rdqa/cobertura?periodo&...` retornando `{ percent, total, gerados, faltantes: [{quadro, motivo}] }`.
- [x] Testes: diferentes combinações (0%, parcial, 100%).
  - `backend/tests/test_rdqa_cobertura.py`.

## 4) Diff entre Ciclos (Atual vs Anterior)
- [ ] Serviço: comparar valores de indicadores entre dois períodos.
  - `app/services/rdqa_diff_service.py` com `comparar(indicadores, periodo_atual, periodo_anterior)` retornando `valor_atual`, `valor_anterior`, `delta`, `tendencia` (`melhora`/`piora`/`igual`).
- [ ] Rota API: `GET /rdqa/diff?periodo_atual&periodo_anterior&indicadores=...`.
- [ ] Testes: casos de melhora, piora e estabilidade.
  - `backend/tests/test_rdqa_diff.py`.

## 5) Pacote de Reprodutibilidade
- [ ] Serviço para empacotar dados, scripts e metadados em `.zip`.
  - `app/services/reproducibilidade_service.py` com `gerar_pacote(exec_id | periodo | filtros)`:
    - Exportar CSV/JSON das dimensões e fatos necessários.
    - Incluir `SQL seeds` mínimos (estrutura e inserts essenciais).
    - `README.md` com passos de reprodução e versão do app.
    - `MANIFEST.json` com `exec_id`, `hash`, `fonte`, `periodo`, `versao`, timestamp e checksums por arquivo.
- [ ] Rota API: `POST /rdqa/export/pacote` retornando `application/zip` e cabeçalhos com proveniência (`X-Exec-Id`/`X-Hash`).
- [ ] Testes: validar estrutura do `.zip` e manifest; checar presença dos principais arquivos.
  - `backend/tests/test_reproducibilidade.py`.

## 6) Integrações, Segurança e Config
- [ ] Headers de proveniência: manter `X-Exec-Id` e `X-Hash` em exportações; registrar no banco quando aplicável.
- [ ] Chave de API: exigir `X-API-Key` nas rotas de escrita/geração, quando `API_KEY` estiver definida no ambiente.
- [ ] CORS/ambiente: garantir `ALLOWED_ORIGINS` no `.env`. Confirmar `DATABASE_URL` e Alembic em Postgres.
- [ ] Observabilidade (opcional): logs estruturados com `exec_id` para rastrear cada geração.

## 7) OpenAPI e Documentação
- [ ] Documentar novos endpoints (`/public/verificar`, `/rdqa/consistencia`, `/rdqa/cobertura`, `/rdqa/diff`, `/rdqa/export/pacote`) com exemplos de request/response e headers.
- [ ] Incluir descrições de parâmetros (filtros, períodos) e códigos de erro (400/404/409/500) em `app/api/routes/*`.
- [ ] Atualizar `backend/README.md` com fluxo de verificação pública e reprodutibilidade.

## 8) Alinhamento com o Frontend
- [ ] Verificação: backend responde para a página `/public/verificar` com `ok`, metadados e mensagens claras.
- [ ] Consistência: endpoints de MAPE entregam dados prontos para cards e drill-down.
- [ ] Cobertura: retornar `{percent, faltantes[motivo]}` para o componente de progresso/lista.
- [ ] Diff: retornar `tendencia` (`melhora/piora/igual`) e deltas prontos para visualização.
- [ ] Exportações: manter headers `X-Exec-Id`/`X-Hash` para composição do QR Code no PDF.

## 9) Entrega e Testes
- [ ] Executar `cd backend && pytest -q` e cobrir novos testes.
- [ ] Postgres: `set DATABASE_URL=... && alembic upgrade head` para criar/alterar tabelas novas.
- [ ] Validar manualmente exportações (PDF e pacote `.zip`) e a verificação pública.

---

Notas
- O endpoint `POST /rdqa/export/pdf` registra execuções e retorna `X-Exec-Id`/`X-Hash` (ver `backend/app/api/routes/rdqa.py`). A verificação pública está implementada em `backend/app/api/routes/public.py`.
- Siga o padrão de camadas do repositório; concentre regras nos `services/` e mantenha rotas finas.
- Em dev (SQLite), migrações Alembic podem ser simuladas por seeds; em prod (Postgres), use migrações.
