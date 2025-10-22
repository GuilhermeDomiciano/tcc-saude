# Plano de Implementação para Cobrir Lacunas RDQA/RAG

Documento de trabalho que destrincha, em etapas executáveis, tudo que está faltando para que a plataforma atenda ao resumo do projeto (pipeline reprodutível, auditável e rastreável da planilha aos painéis RDQA e RAG, com redução comprovável de retrabalho). **Enquanto funcionalidades do backend estiverem em construção, priorizar prototipagem no frontend com dados mockados** (fixtures locais, JSON estático ou MSW) para validar layout, fluxo e interações antes da disponibilização real da API.

## 1. Diagnóstico das Lacunas Atuais
- **RAG inexistente (end-to-end):**
  - Backend não possui schemas, serviços ou rotas para RAG; inspeção de `backend/app/api/routes` mostra apenas módulos RDQA e dimensões básicas.
  - Frontend não tem páginas sob `src/pages/rag/`; somente RDQA e CRUDs de dimensões, logo não há visualização nem exportação RAG.
- **Ingestão oficial ausente / ETL manual:**
  - `backend/app/models/stage.py` define `RawIngest`, porém nenhum worker/serviço consome ou popula essa tabela.
  - `backend/scripts/seed.py` gera dados sintéticos (SQLite) em vez de importar planilhas oficiais; não há pipelines configurados.
- **Indicadores materializados apenas via mocks:**
  - Dados de referência (`DevRefIndicador`, `DevCalcIndicador`) estão em `backend/app/models/dev_lite.py` e são inseridos diretamente em testes (`backend/tests/test_rdqa_consistencia.py`, `test_rdqa_diff.py`).
  - Falta job que calcule indicadores a partir de fontes brutas ou DW; o schema `dw` não contém fatos RDQA/RAG consolidados.
- **Dashboards e UX restritos:**
  - Frontend limita-se a tabelas das dimensões e três telas RDQA (`src/pages/rdqa/*`); não há gráficos comparativos, visão executiva ou integração com RAG.
  - Página inicial (`frontend/src/pages/Dashboard.tsx`) é placeholder e não exibe métricas chave (cobertura, MAPE, tempo de processamento).
- **Proveniência parcial:**
  - `ArtefatoService` registra apenas exportações RDQA (`app/services/artefato_service.py`), mas ingestões/transformações não geram artefatos nem relacionam hashes das fontes.
  - `/public/verificar` cobre somente PDFs RDQA; não há verificação para pacotes RAG ou logs ETL.
- **Métricas de produtividade e retrabalho ausentes:**
  - Projeto carece de logs estruturados com tempos por etapa; nenhum endpoint expõe redução de horas ou comparativos com processos manuais.
  - Não existem tabelas DW dedicadas a capturar métricas operacionais (tempo de ciclo, sucessos/falhas, número de repetições).

## 2. Pipeline de Dados (Planilha ➔ Stage ➔ DW)
1. **Contrato de planilhas oficiais**
   - Inventariar fontes (RDQA e RAG): versões, layout, dicionário de colunas.
   - Definir esquema JSON para captura bruta em `stage.raw_ingest`.
   - Documentar contratos e validações no repositório (`backend/db/README`).
2. **Ingestão bruta**
   - Implementar worker/CLI (`backend/app/workers/ingest_rdqa.py`) que:
     1. Lê arquivos (CSV/XLSX) ou APIs oficiais.
     2. Normaliza cabeçalhos, registra metadados (fonte, período, checksum).
     3. Persiste JSON em `stage.RawIngest` e salva arquivo em storage versionado.
   - Adicionar testes unitários com fixtures de planilhas reais/sintéticas.
3. **Transformação para Stage estruturado**
   - Criar modelos `stage.RefIndicador` e `stage.CalcIndicador` via ETL parametrizado:
     - `RefIndicador`: valores de referência (planilha oficial).
     - `CalcIndicador`: valores recalculados a partir de dados primários.
   - Armazenar histórico por período e chave dimensional.
4. **Carga para DW**
   - Desenvolver job incremental (`backend/app/workers/load_dw.py`) que:
     - Harmoniza chaves (município/unidade/período) com dimensões `dw.*`.
     - Materializa fatos RDQA e RAG em tabelas analíticas (ex.: `dw.fato_rdqa`, `dw.fato_rag`).
   - Em Postgres, criar views/materialized views para indicadores compostos.
5. **Orquestração**
   - Configurar pipeline com Dagster/Airflow ou cron + scripts:
     - Etapas: ingestão ➔ validação ➔ stage ➔ DW ➔ geração de indicadores.
   - Registrar execuções com `artefatos` (exec_id/hash) e logs estruturados (JSON).

## 3. Indicadores RDQA e RAG
1. **Catálogo de indicadores**
   - Consolidar dicionário (nome, fórmula, denominadores, fonte) e armazenar em `dw.dim_indicador`.
2. **Motor de cálculo**
   - Implementar serviço `IndicadorService` que lê dados do stage/DW e calcula:
     - Cobertura, consistência e diffs (já existentes, reaproveitar).
     - Indicadores RAG (financeiros, produção, metas) com regras declarativas (YAML/JSON).
   - Persistir resultados em `dw.fato_indicador` com colunas: indicador, chave, período, valor, proveniência.
3. **Validação automática**
   - Comparar `Calc` x `Ref` com regras de tolerância (MAPE, limites absolutos).
   - Gerar relatórios de divergência por indicador/período, salvando em `artefatos`.

## 4. Cobertura Completa de RDQA
1. **Revisar serviços existentes**
   - Garantir que `ConsistenciaService`, `RDQACoberturaService` e `RDQADiffService` operem sobre dados reais (não só dev_lite).
   - Adicionar filtros por território, unidade, equipe.
2. **Exportação PDF**
   - Melhorar `RDQAExportService` com:
     - Pool de browser e retentativas.
     - Inclusão automática de QR (exec_id/hash) numa única chamada: gerar HTML, inserir QR antes do PDF.
3. **API & testes**
   - Cobrir casos de erro (timeout, falta de dados).
   - Tests de integração que simulam pipeline completo (seed real ➔ ETL ➔ API).

## 5. Implementação do RAG
1. **Modelagem**
   - Criar tabelas `dw.fato_rag_financeiro`, `dw.fato_rag_producao`, `dw.fato_rag_metas` (segundo escopo municipal).
   - Definir schemas Pydantic para entrada/saída (`app/schemas/rag.py`).
2. **Serviços**
   - `RAGService` com métodos:
     - `resumo(periodo, territorio)`
     - `detalhes_financeiro(...)`, `detalhes_producao(...)`, etc.
     - `gerar_pdf(...)` reutilizando infraestrutura RDQA.
3. **Rotas**
   - `GET /rag/resumo`, `GET /rag/{quadro}`, `POST /rag/export/pdf`, `POST /rag/export/pacote`.
   - Exigir `X-API-Key` em operações de escrita/geração.
4. **Testes**
   - `backend/tests/test_rag_*.py` cobrindo:
     - Resumo consolidado.
     - Drill-down por indicador.
     - Exportações com headers de proveniência.
5. **Integração com pipeline**
   - Garantir que ETL populará dados necessários antes de expor endpoints.

## 6. Frontend: Dashboards RDQA + RAG
1. **Arquitetura**
   - Criar `src/pages/rag/` com subpáginas: `Resumo`, `Financeiro`, `Produção`, `Metas`.
   - Ajustar `router.tsx` para rotas `/rag/...`.
2. **Componentes compartilhados**
   - Reaproveitar `DataTable`, `Provenance` e helpers de exportação.
   - Criar gráfico (Recharts/ECharts) para tendências e diffs entre períodos.
3. **Fluxo de exportação**
   - Adicionar botão “Exportar PDF” em cada quadro RAG; usar mesma função de QR com endpoints RAG.
4. **Estado global de dados**
   - Usar React Query para RDQA/RAG com cache e revalidação automática após ETL.
5. **Acessibilidade e UX**
   - Implementar melhorias pendentes: focus trap, mensagens vazias, tooltips.
   - Mostrar badges de proveniência (fonte/periodicidade/exec_id) em cards.
6. **Testes frontend**
   - Adicionar Vitest + Testing Library para tabelas e exportações (mock de API).
   - Cobrir geração de QR e leitura de headers.

## 7. Proveniência, Auditoria e Observabilidade
1. **Metadados padronizados**
   - Estender `ArtefatoService` para registrar etapa (ingestão, transformação, exportação), inputs (hash das planilhas) e outputs.
   - Adicionar tabela `dw.log_execucao` para tracking de jobs ETL (status, duração, operador).
2. **QR Code & Verificação**
   - Expandir `/public/verificar` para aceitar tipo (`rdqa_pdf`, `rag_pdf`, `etls`), retornando detalhes (fonte, período, hash de origem).
   - Criar página pública no frontend `/verificar` para consulta pelo QR.
3. **Logs estruturados**
   - Configurar logging JSON em FastAPI e workers (correlação por `exec_id`).
   - Enviar logs para stack ELK/CloudWatch ou armazenar em `logs/`.
4. **Alertas**
   - Definir thresholds (MAPE > X%, cobertura < Y%) e emitir alertas via e-mail/Slack.

## 8. Métricas de Retrabalho e Consistência
1. **Baseline manual**
   - Medir tempo atual gasto na atualização (coleta, limpeza, publicação).
2. **Medições automáticas**
   - Registrar duração de cada etapa do pipeline (`stage`, `dw`, exportação).
   - Expor endpoint `/metrics` com dados agregados (pode usar Prometheus).
3. **Relatórios comparativos**
   - Geração automática de relatório quadrimestral comparando esforço manual pré vs pós-automação.
   - Persistir no DW (tabela `dw.exec_metricas`) e disponibilizar no frontend.

## 9. Documentação e Governança
1. **Docs técnicos**
   - Atualizar `backend/README.md`, `frontend/README.md` e criar `/docs/pipeline.md` explicando:
     - Estrutura do ETL, contratos de dados, fluxos RDQA/RAG.
   - Adicionar diagramas (plantuml/draw.io) de arquitetura e lineage.
2. **Procedimentos operacionais**
   - Criação de runbooks (como reprocessar período, como validar diff).
   - Checklist de publicação quadrimestral.
3. **Compliance**
   - Revisar requisitos legais de transparência (LGPD, legislação municipal).
   - Garantir anonimização quando necessário em datasets publicados.

## 10. Automação, CI/CD e Entregáveis
1. **CI Pipeline**
   - Configurar GitHub Actions (ou equivalente) com jobs:
     - Lint + testes backend (pytest).
     - Lint + testes frontend (Vitest).
     - Execução de ETL em small dataset (smoke).
     - Build frontend.
2. **CD**
   - Automatizar deploy backend (Docker + migrations + seeds controlados).
   - Automatizar deploy frontend (build + publicação em ambiente público).
3. **Artefatos**
   - Armazenar pacotes PDF/ZIP gerados em storage versionado com metadata.
   - Incluir QR nas versões públicas disponibilizadas.

## 11. Roadmap Sugerido
| Semana | Entregas principais |
| --- | --- |
| 1 | Contratos de dados, ingestão bruta e storage versionado |
| 2 | Transformações Stage ➔ DW + motor de indicadores RDQA |
| 3 | Implementação RAG (modelos, serviços, API, testes) |
| 4 | Dashboards RDQA/RAG completos + exportações com QR |
| 5 | Métricas de retrabalho, observabilidade, alertas |
| 6 | Documentação final, CI/CD, validação com stakeholders |

## 12. Validação Final
- Executar pipeline completo com dados reais de pelo menos um ciclo quadrimestral.
- Comparar automaticamente com planilhas oficiais e arquivar relatórios de divergência.
- Coletar feedback das secretarias de saúde (usuários finais) sobre redução de retrabalho.
- Firmar checklists de auditoria para cada entrega (dados, dashboards, PDFs, logs).

> Seguindo as etapas acima, a plataforma passa a cumprir integralmente o resumo do projeto: pipeline reprodutível e rastreável, geração automática de RDQA e RAG, dashboards e PDFs auditáveis, além de métricas objetivas de consistência e produtividade.
