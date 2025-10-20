-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE dw.demo_item (
  id bigint NOT NULL DEFAULT nextval('dw.demo_item_id_seq'::regclass),
  nome text NOT NULL,
  valor integer NOT NULL DEFAULT 0,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT demo_item_pkey PRIMARY KEY (id)
);
CREATE TABLE dw.dim_equipe (
  id bigint NOT NULL DEFAULT nextval('dw.dim_equipe_id_seq'::regclass),
  id_equipe text NOT NULL UNIQUE,
  tipo text NOT NULL CHECK (tipo = ANY (ARRAY['ESF'::text, 'ESB'::text, 'ACS'::text, 'OUTROS'::text])),
  unidade_id bigint,
  territorio_id bigint,
  ativo boolean NOT NULL DEFAULT true,
  CONSTRAINT dim_equipe_pkey PRIMARY KEY (id),
  CONSTRAINT dim_equipe_unidade_id_fkey FOREIGN KEY (unidade_id) REFERENCES dw.dim_unidade(id),
  CONSTRAINT dim_equipe_territorio_id_fkey FOREIGN KEY (territorio_id) REFERENCES dw.dim_territorio(id)
);
CREATE TABLE dw.dim_fonte_recurso (
  id bigint NOT NULL DEFAULT nextval('dw.dim_fonte_recurso_id_seq'::regclass),
  codigo text NOT NULL UNIQUE,
  descricao text NOT NULL,
  CONSTRAINT dim_fonte_recurso_pkey PRIMARY KEY (id)
);
CREATE TABLE dw.dim_pop_faixa_etaria (
  id bigint NOT NULL DEFAULT nextval('dw.dim_pop_faixa_etaria_id_seq'::regclass),
  territorio_id bigint NOT NULL,
  ano smallint NOT NULL,
  faixa_etaria text NOT NULL,
  sexo character NOT NULL CHECK (sexo = ANY (ARRAY['M'::bpchar, 'F'::bpchar])),
  populacao integer NOT NULL CHECK (populacao >= 0),
  CONSTRAINT dim_pop_faixa_etaria_pkey PRIMARY KEY (id),
  CONSTRAINT dim_pop_faixa_etaria_territorio_id_fkey FOREIGN KEY (territorio_id) REFERENCES dw.dim_territorio(id)
);
CREATE TABLE dw.dim_tempo (
  id bigint NOT NULL DEFAULT nextval('dw.dim_tempo_id_seq'::regclass),
  data date NOT NULL UNIQUE,
  ano smallint NOT NULL,
  mes smallint NOT NULL CHECK (mes >= 1 AND mes <= 12),
  trimestre smallint NOT NULL CHECK (trimestre >= 1 AND trimestre <= 4),
  quadrimestre smallint NOT NULL CHECK (quadrimestre >= 1 AND quadrimestre <= 3),
  mes_nome text,
  CONSTRAINT dim_tempo_pkey PRIMARY KEY (id)
);
CREATE TABLE dw.dim_territorio (
  id bigint NOT NULL DEFAULT nextval('dw.dim_territorio_id_seq'::regclass),
  cod_ibge_municipio character NOT NULL UNIQUE,
  nome text NOT NULL,
  uf character NOT NULL,
  area_km2 numeric,
  pop_censo_2022 integer,
  pop_estim_2024 integer,
  CONSTRAINT dim_territorio_pkey PRIMARY KEY (id)
);
CREATE TABLE dw.dim_unidade (
  id bigint NOT NULL DEFAULT nextval('dw.dim_unidade_id_seq'::regclass),
  cnes character varying NOT NULL UNIQUE,
  nome text NOT NULL,
  tipo_estabelecimento text,
  bairro text,
  territorio_id bigint,
  gestao text,
  CONSTRAINT dim_unidade_pkey PRIMARY KEY (id),
  CONSTRAINT dim_unidade_territorio_id_fkey FOREIGN KEY (territorio_id) REFERENCES dw.dim_territorio(id)
);
CREATE TABLE dw.fato_cobertura_aps (
  id bigint NOT NULL DEFAULT nextval('dw.fato_cobertura_aps_id_seq'::regclass),
  data date NOT NULL,
  tempo_id bigint NOT NULL,
  territorio_id bigint NOT NULL,
  equipe_id bigint,
  tipo_equipe text NOT NULL CHECK (tipo_equipe = ANY (ARRAY['ESF'::text, 'ESB'::text, 'ACS'::text, 'OUTROS'::text])),
  cobertura_percentual numeric NOT NULL CHECK (cobertura_percentual >= 0::numeric AND cobertura_percentual <= 100::numeric),
  pop_coberta_estimada integer CHECK (pop_coberta_estimada >= 0),
  extract_ts timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT fato_cobertura_aps_pkey PRIMARY KEY (id),
  CONSTRAINT fato_cobertura_aps_tempo_id_fkey FOREIGN KEY (tempo_id) REFERENCES dw.dim_tempo(id),
  CONSTRAINT fato_cobertura_aps_territorio_id_fkey FOREIGN KEY (territorio_id) REFERENCES dw.dim_territorio(id),
  CONSTRAINT fato_cobertura_aps_equipe_id_fkey FOREIGN KEY (equipe_id) REFERENCES dw.dim_equipe(id)
);
CREATE TABLE dw.fato_eventos_vitais (
  id bigint NOT NULL DEFAULT nextval('dw.fato_eventos_vitais_id_seq'::regclass),
  data date NOT NULL,
  tempo_id bigint NOT NULL,
  territorio_id bigint NOT NULL,
  nascidos_vivos integer NOT NULL DEFAULT 0 CHECK (nascidos_vivos >= 0),
  obitos_gerais integer CHECK (obitos_gerais >= 0),
  fonte text,
  extract_ts timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT fato_eventos_vitais_pkey PRIMARY KEY (id),
  CONSTRAINT fato_eventos_vitais_tempo_id_fkey FOREIGN KEY (tempo_id) REFERENCES dw.dim_tempo(id),
  CONSTRAINT fato_eventos_vitais_territorio_id_fkey FOREIGN KEY (territorio_id) REFERENCES dw.dim_territorio(id)
);
CREATE TABLE dw.fato_financas (
  id bigint NOT NULL DEFAULT nextval('dw.fato_financas_id_seq'::regclass),
  data date NOT NULL,
  tempo_id bigint NOT NULL,
  territorio_id bigint NOT NULL,
  fonte_id bigint,
  dotacao_atualizada_anual numeric CHECK (dotacao_atualizada_anual >= 0::numeric),
  receita_realizada numeric CHECK (receita_realizada >= 0::numeric),
  empenhado numeric CHECK (empenhado >= 0::numeric),
  liquidado numeric CHECK (liquidado >= 0::numeric),
  pago numeric CHECK (pago >= 0::numeric),
  extract_ts timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT fato_financas_pkey PRIMARY KEY (id),
  CONSTRAINT fato_financas_tempo_id_fkey FOREIGN KEY (tempo_id) REFERENCES dw.dim_tempo(id),
  CONSTRAINT fato_financas_territorio_id_fkey FOREIGN KEY (territorio_id) REFERENCES dw.dim_territorio(id),
  CONSTRAINT fato_financas_fonte_id_fkey FOREIGN KEY (fonte_id) REFERENCES dw.dim_fonte_recurso(id)
);
CREATE TABLE dw.fato_rede_fisica (
  id bigint NOT NULL DEFAULT nextval('dw.fato_rede_fisica_id_seq'::regclass),
  data date NOT NULL,
  tempo_id bigint NOT NULL,
  territorio_id bigint NOT NULL,
  tipo_unidade text NOT NULL,
  quantidade integer NOT NULL CHECK (quantidade >= 0),
  extract_ts timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT fato_rede_fisica_pkey PRIMARY KEY (id),
  CONSTRAINT fato_rede_fisica_tempo_id_fkey FOREIGN KEY (tempo_id) REFERENCES dw.dim_tempo(id),
  CONSTRAINT fato_rede_fisica_territorio_id_fkey FOREIGN KEY (territorio_id) REFERENCES dw.dim_territorio(id)
);