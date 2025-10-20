-- =====================================================================
--  REDE SAÚDE — CONTEXTO DE ESQUEMA (NÃO EXECUTAR)
--  Objetivo: descrever a estrutura lógica do banco (Supabase/Postgres)
--  para referência de IAs/colaboradores. Os comandos abaixo são
--  ilustrativos; podem não refletir permissões/RLS/índices finais.
-- =====================================================================

-- ---------------------------------------------------------------------
-- DECISÕES DE ARQUITETURA (RESUMO)
-- ---------------------------------------------------------------------
-- * Banco: Supabase Postgres (gerenciado), sem TimescaleDB e sem
--   particionamento por mês (volume atual não exige).
-- * Organização em 2 schemas:
--     - dw     : modelo analítico (dimensões e fatos).
--     - stage  : ingestão bruta (payload JSONB).
-- * Star schema enxuto: 6 dimensões, 4 fatos, 1 tabela de staging.
-- * Índices únicos parciais resolvem chaves “naturais” nas tabelas de fatos
--   quando há colunas opcionais (ex.: fonte_id, equipe_id).
-- * Views utilitárias calculam flags e percentuais (evita colunas geradas).
-- * RLS/Policies: planejadas (leitura em dw.*; escrita apenas service_role;
--   stage.* exclusivo service_role), mas não incluídas aqui.
-- * PostGIS: opcional (geom em dim_territorio/dim_unidade) — fora deste contexto.

-- ---------------------------------------------------------------------
-- SCHEMAS
-- ---------------------------------------------------------------------
-- CREATE SCHEMA dw;
-- CREATE SCHEMA stage;

-- ---------------------------------------------------------------------
-- DIMENSÕES (SCHEMA: dw)
-- ---------------------------------------------------------------------

-- Tempo (grão mensal; flags calculadas via view).
CREATE TABLE dw.dim_tempo (
  id            BIGSERIAL PRIMARY KEY,
  data          DATE NOT NULL UNIQUE,                    -- referência mensal
  ano           SMALLINT NOT NULL,
  mes           SMALLINT NOT NULL CHECK (mes BETWEEN 1 AND 12),
  trimestre     SMALLINT NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
  quadrimestre  SMALLINT NOT NULL CHECK (quadrimestre BETWEEN 1 AND 3),
  mes_nome      TEXT
);

-- Território (IBGE). 'geom' (PostGIS) opcional e fora deste contexto.
CREATE TABLE dw.dim_territorio (
  id                    BIGSERIAL PRIMARY KEY,
  cod_ibge_municipio    CHAR(7) NOT NULL UNIQUE,         -- ex.: '170210'
  nome                  TEXT NOT NULL,                   -- ex.: 'Araguaína'
  uf                    CHAR(2) NOT NULL,                -- ex.: 'TO'
  area_km2              NUMERIC(12,3),
  pop_censo_2022        INTEGER,
  pop_estim_2024        INTEGER
  -- geom geometry(MultiPolygon, 4674)  -- OPCIONAL (PostGIS)
);

-- População por faixa etária e sexo (denominadores específicos).
CREATE TABLE dw.dim_pop_faixa_etaria (
  id              BIGSERIAL PRIMARY KEY,
  territorio_id   BIGINT NOT NULL REFERENCES dw.dim_territorio(id) ON UPDATE CASCADE ON DELETE CASCADE,
  ano             SMALLINT NOT NULL,
  faixa_etaria    TEXT NOT NULL,                          -- '0-4','5-9',...,'80+'
  sexo            CHAR(1) NOT NULL CHECK (sexo IN ('M','F')),
  populacao       INTEGER NOT NULL CHECK (populacao >= 0),
  UNIQUE (territorio_id, ano, faixa_etaria, sexo)
);

-- Unidade de saúde (CNES). 'geom' opcional fora deste contexto.
CREATE TABLE dw.dim_unidade (
  id                    BIGSERIAL PRIMARY KEY,
  cnes                  VARCHAR(7) NOT NULL UNIQUE,
  nome                  TEXT NOT NULL,
  tipo_estabelecimento  TEXT,                             -- 'UBS','UPA','CAPS',...
  bairro                TEXT,
  territorio_id         BIGINT REFERENCES dw.dim_territorio(id) ON UPDATE CASCADE,
  gestao                TEXT
  -- geom geometry(Point, 4674)  -- OPCIONAL (PostGIS)
);

-- Equipes de APS (ESF/ESB/ACS/outras).
CREATE TABLE dw.dim_equipe (
  id            BIGSERIAL PRIMARY KEY,
  id_equipe     TEXT NOT NULL UNIQUE,                     -- id lógico/INE
  tipo          TEXT NOT NULL CHECK (tipo IN ('ESF','ESB','ACS','OUTROS')),
  unidade_id    BIGINT REFERENCES dw.dim_unidade(id) ON UPDATE CASCADE ON DELETE SET NULL,
  territorio_id BIGINT REFERENCES dw.dim_territorio(id) ON UPDATE CASCADE ON DELETE SET NULL,
  ativo         BOOLEAN NOT NULL DEFAULT TRUE
);

-- Fontes de recurso (financeiro).
CREATE TABLE dw.dim_fonte_recurso (
  id        BIGSERIAL PRIMARY KEY,
  codigo    TEXT NOT NULL UNIQUE,                         -- 'FED','EST','MUN','ROY','CONV',...
  descricao TEXT NOT NULL
);

-- ---------------------------------------------------------------------
-- FATOS (SCHEMA: dw)
-- ---------------------------------------------------------------------

-- Eventos vitais (mensal). Unicidade por território+data.
CREATE TABLE dw.fato_eventos_vitais (
  id              BIGSERIAL PRIMARY KEY,
  data            DATE NOT NULL,                          -- competência (mês)
  tempo_id        BIGINT NOT NULL REFERENCES dw.dim_tempo(id) ON UPDATE CASCADE,
  territorio_id   BIGINT NOT NULL REFERENCES dw.dim_territorio(id) ON UPDATE CASCADE,
  nascidos_vivos  INTEGER NOT NULL DEFAULT 0 CHECK (nascidos_vivos >= 0),
  obitos_gerais   INTEGER CHECK (obitos_gerais >= 0),
  fonte           TEXT,                                   -- 'SINASC','SIM',...
  extract_ts      TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (territorio_id, data)
);

-- Finanças (mensal). Chave natural muda se 'fonte_id' for nula ou não.
CREATE TABLE dw.fato_financas (
  id                          BIGSERIAL PRIMARY KEY,
  data                        DATE NOT NULL,              -- competência (mês)
  tempo_id                    BIGINT NOT NULL REFERENCES dw.dim_tempo(id) ON UPDATE CASCADE,
  territorio_id               BIGINT NOT NULL REFERENCES dw.dim_territorio(id) ON UPDATE CASCADE,
  fonte_id                    BIGINT REFERENCES dw.dim_fonte_recurso(id) ON UPDATE CASCADE,
  dotacao_atualizada_anual    NUMERIC(14,2) CHECK (dotacao_atualizada_anual >= 0),
  receita_realizada           NUMERIC(14,2) CHECK (receita_realizada >= 0),
  empenhado                   NUMERIC(14,2) CHECK (empenhado >= 0),
  liquidado                   NUMERIC(14,2) CHECK (liquidado >= 0),
  pago                        NUMERIC(14,2) CHECK (pago >= 0),
  extract_ts                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Índices únicos parciais (lógica de unicidade por competência):
--   - Se fonte_id IS NULL: UNIQUE(territorio_id, data)
--   - Se fonte_id IS NOT NULL: UNIQUE(territorio_id, data, fonte_id)
-- (No Supabase, criar via CREATE UNIQUE INDEX ... WHERE ...)

-- Cobertura APS (mensal). Chave natural muda se 'equipe_id' existe.
CREATE TABLE dw.fato_cobertura_aps (
  id                     BIGSERIAL PRIMARY KEY,
  data                   DATE NOT NULL,
  tempo_id               BIGINT NOT NULL REFERENCES dw.dim_tempo(id) ON UPDATE CASCADE,
  territorio_id          BIGINT NOT NULL REFERENCES dw.dim_territorio(id) ON UPDATE CASCADE,
  equipe_id              BIGINT REFERENCES dw.dim_equipe(id) ON UPDATE CASCADE ON DELETE SET NULL,
  tipo_equipe            TEXT NOT NULL CHECK (tipo_equipe IN ('ESF','ESB','ACS','OUTROS')),
  cobertura_percentual   NUMERIC(5,2) NOT NULL CHECK (cobertura_percentual >= 0 AND cobertura_percentual <= 100),
  pop_coberta_estimada   INTEGER CHECK (pop_coberta_estimada >= 0),
  extract_ts             TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Índices únicos parciais para cobertura:
--   - equipe_id IS NULL     : UNIQUE(territorio_id, tipo_equipe, data)
--   - equipe_id IS NOT NULL : UNIQUE(territorio_id, equipe_id, tipo_equipe, data)

-- Rede física (mensal). Unicidade por território+tipo_unidade+data.
CREATE TABLE dw.fato_rede_fisica (
  id               BIGSERIAL PRIMARY KEY,
  data             DATE NOT NULL,
  tempo_id         BIGINT NOT NULL REFERENCES dw.dim_tempo(id) ON UPDATE CASCADE,
  territorio_id    BIGINT NOT NULL REFERENCES dw.dim_territorio(id) ON UPDATE CASCADE,
  tipo_unidade     TEXT NOT NULL,        -- 'UBS','UPA','CAPS','POLICLINICA','LEITOS_CLINICOS','LEITOS_UTI',...
  quantidade       INTEGER NOT NULL CHECK (quantidade >= 0),
  extract_ts       TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (territorio_id, tipo_unidade, data)
);

-- ---------------------------------------------------------------------
-- STAGING (SCHEMA: stage)
-- ---------------------------------------------------------------------

-- Ingestão bruta de arquivos (RDQA/planilhas/etc.) em JSONB.
CREATE TABLE stage.raw_ingest (
  id            UUID PRIMARY KEY,         -- gerado na aplicação
  fonte         TEXT NOT NULL,            -- 'RDQA_2025_Q1','PRODATA','SINASC',...
  periodo_ref   TEXT NOT NULL,            -- '2025-Q1','2025-01',...
  payload       JSONB NOT NULL,
  ingested_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------
-- VIEWS UTILITÁRIAS (SCHEMA: dw)
-- ---------------------------------------------------------------------

-- Denominador padrão: preferir Estimativa 2024; fallback Censo 2022.
CREATE VIEW dw.vw_denominador_populacao AS
SELECT
  t.id AS territorio_id,
  t.cod_ibge_municipio,
  t.nome,
  t.uf,
  COALESCE(t.pop_estim_2024, t.pop_censo_2022) AS pop_denominador,
  t.pop_censo_2022,
  t.pop_estim_2024,
  t.area_km2
FROM dw.dim_territorio t;

-- Flags de calendário (evita colunas GENERATED).
CREATE VIEW dw.vw_dim_tempo_flags AS
SELECT
  d.*,
  (d.data = (date_trunc('month', d.data) + INTERVAL '1 month - 1 day')::date) AS fim_de_mes,
  (EXTRACT(MONTH FROM d.data)::INT IN (1,5,9))                                  AS inicio_qd
FROM dw.dim_tempo d;

-- Execução financeira: percentuais úteis para dashboards/relatórios.
CREATE VIEW dw.vw_financas_execucao AS
SELECT
  f.id, f.data, f.tempo_id, f.territorio_id, f.fonte_id,
  f.dotacao_atualizada_anual, f.receita_realizada, f.empenhado, f.liquidado, f.pago, f.extract_ts,
  CASE WHEN f.liquidado > 0 THEN ROUND((f.pago / f.liquidado) * 100.0, 2) ELSE NULL END AS pct_pago_sobre_liquidado,
  CASE WHEN f.dotacao_atualizada_anual > 0 THEN ROUND((f.empenhado / f.dotacao_atualizada_anual) * 100.0, 2) ELSE NULL END AS pct_empenhado_sobre_dotacao
FROM dw.fato_financas f;

-- ---------------------------------------------------------------------
-- ÍNDICES (IDEIA GERAL — CRIAR NO DB REAL, NÃO AQUI)
-- ---------------------------------------------------------------------
-- Exemplos (não executar neste arquivo de contexto):
--   -- Dimensões
--   CREATE INDEX ix_dim_tempo_ano_mes            ON dw.dim_tempo (ano, mes);
--   CREATE INDEX ix_dim_territorio_uf            ON dw.dim_territorio (uf);
--   CREATE INDEX ix_dim_pop_faixa_territorio_ano ON dw.dim_pop_faixa_etaria (territorio_id, ano);
--   -- Fatos
--   CREATE INDEX ix_fev_territorio_data_desc     ON dw.fato_eventos_vitais (territorio_id, data DESC);
--   -- Finanças (unicidade parcial)
--   CREATE UNIQUE INDEX ux_ffin_null    ON dw.fato_financas (territorio_id, data) WHERE fonte_id IS NULL;
--   CREATE UNIQUE INDEX ux_ffin_notnull ON dw.fato_financas (territorio_id, data, fonte_id) WHERE fonte_id IS NOT NULL;
--   -- Cobertura (unicidade parcial)
--   CREATE UNIQUE INDEX ux_fcap_null    ON dw.fato_cobertura_aps (territorio_id, tipo_equipe, data) WHERE equipe_id IS NULL;
--   CREATE UNIQUE INDEX ux_fcap_notnull ON dw.fato_cobertura_aps (territorio_id, equipe_id, tipo_equipe, data) WHERE equipe_id IS NOT NULL;

-- ---------------------------------------------------------------------
-- DADOS ESSENCIAIS (DO RDQA) — COMO ESSES CAMPOS ENTRAM
-- ---------------------------------------------------------------------
-- * Demografia (IBGE): area_km2, pop_censo_2022, pop_estim_2024 → dw.dim_territorio.
--   Por sexo/faixa etária → dw.dim_pop_faixa_etaria (denominadores).
-- * Eventos vitais (nascidos vivos, óbitos) → dw.fato_eventos_vitais.
-- * Cobertura APS (ESF/ESB) e equipes/ACS → dw.fato_cobertura_aps e dw.dim_equipe.
-- * Rede física (UBS/UPA/CAPS/leitos) → dw.fato_rede_fisica + dw.dim_unidade (opcional).
-- * Financeiro (dotação, receita, empenhado/liquidado/pago) → dw.fato_financas; percentuais via dw.vw_financas_execucao.

-- ---------------------------------------------------------------------
-- BUCKET (SUPABASE STORAGE) — ACESSO RECOMENDADO
-- ---------------------------------------------------------------------
-- * Buckets privados: backend gera URL assinada (expira) via endpoint:
--   POST /storage/v1/object/sign/{bucket}/{path} (usa service_role no backend).
-- * Frontend consome apenas a URL assinada (sem expor chaves).

-- ---------------------------------------------------------------------
-- DEMO (APENAS PARA TESTE DE CONEXÃO; NÃO FAZ PARTE DO DW)
-- ---------------------------------------------------------------------
-- CREATE TABLE dw.demo_item (
--   id BIGSERIAL PRIMARY KEY,
--   nome TEXT NOT NULL,
--   valor INTEGER NOT NULL DEFAULT 0,
--   created_at timestamptz NOT NULL DEFAULT now()
-- );
-- INSERT INTO dw.demo_item (nome, valor) VALUES ('Item A',10),('Item B',20),('Item C',30);

-- =====================================================================
--  FIM DO ARQUIVO DE CONTEXTO (NÃO EXECUTAR)
-- =====================================================================
