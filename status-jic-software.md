# STATUS — Plataforma RDQA/RAG × Artigo para a JIC
**Data:** 2025-10-21 · **Responsável:** Domiciano · **Versão:** 0.1

Este documento conecta o **estado do software** (Agents.md, implementacao-backend.md, implementacao-frontend.md) ao **artigo da JIC**, servindo como **contexto único** para decisões, entregas e escrita científica.

---

## 1) Objetivo do status.md
- Alinhar **o que o sistema faz** com **como vamos descrever e avaliar** no artigo.
- Definir **artefatos obrigatórios** (Figuras/Tabelas) e **quem/onde** serão produzidos no código.
- Registrar **lacunas** e **próximas ações** focadas na submissão da JIC.

---

## 2) Visão geral do produto (do _Agents.md_)
- **Nome/escopo:** Plataforma municipal de transparência em saúde para **RDQA** e **RAG** (pipeline reprodutível, auditável e versionado).
- **Arquitetura:** Backend **FastAPI + SQLModel + PostgreSQL** (schemas `stage` e `dw`), **Alembic** para migração, serviços e repositórios; Frontend **React + Vite + TS + Tailwind + shadcn/ui**.
- **Segurança/ops:** `X-API-Key` opcional para escrita, CORS configurado, logs padronizados.
- **Entrega:** API REST (`/dw/*`), dashboards e **exportação em PDF** (Pyppeteer/WeasyPrint), testes automatizados, Docker/Compose/Traefik.

> **Ideia central para o artigo:** “**Pipeline reprodutível** da planilha às tabelas RDQA/RAG, com **proveniência ponta a ponta** e **métricas objetivas** de consistência e produtividade.”

---

## 3) O que já FOI feito (do _implementacao-backend.md_)
- **Modelagem & Schemas:** `stage` (zona bruta/normalizada) e `dw` (mart de indicadores). Dimensões já implementadas: **Território**, **Tempo**, **População por Faixa Etária**, **Unidade**, **Equipe**, **Fonte de Recurso**.
- **Camadas:** engine/sessão, repositórios, serviços com validações, rotas **`/dw/*`** com paginação/filtros; **tratamento de erros** consistente.
- **Infra:** migração inicial com Alembic, _seed_ de desenvolvimento, **testes de API**.
- **Autorização:** `X-API-Key` para rotas críticas de escrita ou cargas.

**Observação para o artigo:** estes elementos suportam as seções de **Ingestão/Normalização/Validação**, **Materialização** e **Publicação/Serviços** em _Procedimentos_.

---

## 4) O que VAI ser feito (do _implementacao-frontend.md_)
- **Páginas (MVP):** `/` (Resumo), `/tempo`, `/territorios`, `/pop-faixa`, `/unidades`, `/equipes`, `/fontes`.
- **Tabelas/UX:** React Table + TanStack Query; **Formulários** com RHF + Zod; **badges de proveniência** (fonte/período/versão) nos cards/tabelas.
- **Exportação:** páginas de **Quadros RDQA** com **geração de PDF**.
- **Testes:** Vitest + Testing Library; build Docker.

**Observação para o artigo:** telas e PDFs compõem a seção **Publicação/Serviços**; _prints_ podem entrar como **Figuras adicionais** em Anexo, se necessário.

---

## 5) Mapa de alinhamento — Software → Artigo (JIC)

| Seção do Artigo | Evidência no Software | Arquivos/Rotas | Artefato no Paper |
|---|---|---|---|
| **Desenho do estudo** (Design Science + estudo de caso) | Justificativa e objetivos no Agents.md | — | Texto (sem figuras) |
| **Dados e amostra** | Catálogo de fontes e períodos (IBGE, SIM, SINASC, e-SUS, CNES, SIAF/SIOPS…) | `stage.*` + docs de ETL | Texto (sem figuras) |
| **3.1 Visão geral do pipeline** | Arquitetura end-to-end e camadas | Agents.md + módulos `core/api/models/services` | **Figura 1** — Arquitetura geral |
| **3.2 Ingestão/Normalização/Validação** | Regras de normalização/consistência e proveniência | `stage.*`, serviços de ETL | Texto técnico (sem figuras) |
| **3.3 Materialização de indicadores** | _Mart_ em `dw.*`, views e dicionário de indicadores | `/dw/*` (GET) | **Tabela 1** — Dicionário operacional |
| **3.4 Rastreabilidade ponta a ponta** | Metadados (fonte/período/versão), carimbos de execução | logs e tabelas auxiliares | **Figura 2** — Linhagem/proveniência |
| **3.5 Publicação/Serviços** | API paginada, cache, exportação PDF | FastAPI `/dw/*` + exporter | Texto + prints em Anexo (opcional) |
| **3.6 Orquestração/Agendamentos** | Jobs (Redis/RQ) e tempos por etapa | workers & schedulers | **Figura 3** — Fluxo ETL e tempos |
| **Métricas/Análises** | Logs + diffs vs. planilhas de referência | scripts de validação | Texto referenciando **Figura 3** |

---

## 6) Artefatos obrigatórios (para a JIC) — donos e status
> Preencha os donos entre parênteses e marque o status.

- [ ] **Figura 1 — Arquitetura geral do pipeline RDQA/RAG** (owner: …) · **onde gerar:** diagrama (Draw.io/Excalidraw/Figma) a partir do Agents.md.
- [ ] **Tabela 1 — Dicionário operacional de indicadores (recorte)** (owner: …) · **onde gerar:** planilha → Markdown/LaTeX (7 colunas padrão).
- [ ] **Figura 2 — Linhagem de dados / proveniência célula→indicador** (owner: …) · **onde gerar:** diagrama com nós (indicador → fatos → fontes).
- [ ] **Figura 3 — Fluxo ETL & orquestração (tempos típicos)** (owner: …) · **onde gerar:** fluxograma/swimlanes + tempos médios por etapa.
- [ ] **Seção de Métricas** (owner: …) · **como obter:** logs ETL + _diff_ com planilhas oficiais + tempos P95 de API.

---

## 7) Métricas: definição operacional (para o paper e para o sistema)
- **Consistência:** MAPE das saídas vs. planilhas oficiais (por indicador/quadro e período).
- **Cobertura:** % de quadros RDQA/RAG gerados automaticamente.
- **Produtividade:** horas economizadas por ciclo (baseline manual × pipeline).
- **Atualidade:** dias do dado mais recente até publicação (ingestão→entrega).
- **Desempenho:** tempo total de ETL por ciclo; **latência P95** das rotas `/dw/*`.

> **Fontes de verdade para métricas:** logs de execução (ETL), metadados de proveniência, benchmarks das rotas e _diff_ com planilhas-referência.

---

## 8) Checklist técnico para sustentar as métricas
- [ ] Registrar **ID de execução** e **hash** por carga (amarrar `stage`→`dw`→exportação).
- [ ] Persistir **tempos por etapa** (ingestão, normalização, materialização, publicação).
- [ ] Implementar _endpoint_ de **health/metrics** para exportar tempos/agregados (prometheus/json).
- [ ] Script de **validação** que compara pipeline vs. planilhas (gera MAPE/erros e _diff_).

---

## 9) Riscos e mitigação (foco JIC)
- **Dados inconsistentes ou tardios**: usar _freezes_ por período e hashes de arquivo; documentar desvios.
- **Escopo do frontend**: priorizar **telas RDQA** e **exportação PDF**; _prints_ podem suprir telas faltantes no paper.
- **Tempo de coleta de métricas**: executar **pipeline em ambiente limpo** (reprodutibilidade) e medir em lote.

---

## 10) Próximas ações (curto prazo, orientadas ao paper)
1) Fechar o **recorte de indicadores** do MVP para a **Tabela 1**.  
2) Diagramar **Figura 1** (arquitetura) e **Figura 2** (linhagem).  
3) Instrumentar **tempos por etapa** e gerar **Figura 3** (fluxo ETL).  
4) Rodar script de **consistência (MAPE)** e preencher seção de **Métricas**.  
5) Preparar **página de Quadros RDQA** e **exportação PDF** para prints.

---

## 11) MATERIAL E MÉTODOS — template pronto (colar no artigo)
> **Ordem e conteúdo fornecidos pelo “contexto adicional”**. Substitua colchetes e insira imagens onde indicado.

**Desenho do estudo.** Pesquisa de engenharia de artefatos orientada por Design Science, combinada a estudo de caso com dados secundários públicos do SUS.

**Dados e amostra.** Dados agregados (IBGE, SINASC, SIM, SINAN, SISAB/e-SUS AB, CNES, PNI/LocalizaSUS, SIAF/SIOPS), séries anuais/quadrimestrais (2014–2025).

**Procedimentos.**  
**Visão geral do pipeline.** O sistema foi estruturado em etapas sequenciais (ingestão, normalização, validação, materialização de indicadores, publicação e entrega), com rastreabilidade ponta a ponta (ver Figura 1).

[INSERIR FIGURA 1 AQUI]  
**Figura 1 – Arquitetura geral do pipeline RDQA/RAG.**  
_Fonte: elaboração própria._  
*Explicação:* A figura apresenta, da esquerda para a direita, as fontes oficiais, a zona bruta de ingestão (com metadados e hash), a normalização/validação, o “mart” de indicadores, a API e as camadas de entrega (dashboards e exportação em PDF), destacando pontos de auditoria.

**Ingestão, normalização e validação.** Arquivos são padronizados (codificação, datas ISO 8601), recebem metadados de proveniência e passam por regras de consistência (subtotais, faixas percentuais, reconciliação inter-sistemas).

**Materialização de indicadores.** Cada indicador possui nome, definição, numerador, denominador, unidade/escala, periodicidade e fonte. As fórmulas canônicas incluem, por exemplo, incidência (casos/população·100 000) e mortalidade geral (óbitos/população·1000). A Tabela 1 resume um recorte do dicionário operacional.

[INSERIR TABELA 1 AQUI]  
**Tabela 1 – Dicionário operacional de indicadores (recorte).**  
_Fonte: elaboração própria._  
*Explicação:* A tabela padroniza definições e insumos de cálculo (numerador/denominador), garantindo comparabilidade temporal e entre fontes.

**Rastreabilidade ponta a ponta.** Cada transformação recebe um identificador de execução, e as células calculadas mantêm referência à fonte/período/versão do dado original (ver Figura 2).

[INSERIR FIGURA 2 AQUI]  
**Figura 2 – Linhagem de dados e proveniência célula → indicador.**  
_Fonte: elaboração própria._  
*Explicação:* O diagrama ilustra como um valor final (ex.: “Mortalidade geral 2024”) aponta para tabelas de fato e, destas, para os arquivos fonte versionados.

**Publicação/serviços.** Endpoints REST (FastAPI) com cache e paginação; autenticação; exportação de quadros/tabelas do RDQA/RAG em PDF com QR Code de verificação.

**Orquestração e tarefas agendadas.** Cargas e recomputações são agendadas (ex.: Redis/RQ). A Figura 3 resume o fluxo e tempos típicos por etapa.

[INSERIR FIGURA 3 AQUI]  
**Figura 3 – Fluxo ETL e orquestração de tarefas (tempos típicos).**  
_Fonte: elaboração própria._  
*Explicação:* O fluxograma evidencia as etapas (Ingerir → Transformar → Materializar → Publicar → Entregar) e tempos médios de execução usados nas métricas de produtividade.

**Métricas de avaliação/Análises.** Consistência (MAPE vs. planilhas oficiais), cobertura (% de quadros RDQA/RAG gerados), produtividade (horas economizadas), atualidade (dias até atualização publicada) e desempenho (tempo ETL; latência P95). As métricas de produtividade se baseiam nos tempos exibidos na Figura 3.

**Ética.** Dados públicos agregados, sem identificação pessoal, sem risco adicional; dispensa submissão a CEP/CONEP.

**Unidades e símbolos (SI).** Proporções em %; taxas por 1 000 hab. e 100 000 hab.; tempo em h/min; valores em BRL (R$); coordenadas em ° (graus decimais).

**Regra ABNT prática:** figuras e tabelas ficam sempre o mais perto possível da primeira menção. Numere como **Figura 1, 2, 3…** e **Tabela 1, 2…** (numerações independentes). Abaixo de cada uma: **legenda + Fonte:** …. Em seguida, 1–2 frases explicando o que ela mostra.

---

## 12) Guia rápido para montar as figuras/tabelas
- **Figura 1 (Arquitetura):** blocos horizontais com setas → Fontes → Ingestão/Raw (metadados + hash) → Normalização/Validação → Mart de Indicadores (views) → API → Dashboards/PDF. Realce “Proveniência” atravessando todas as etapas.
- **Tabela 1 (Dicionário):** 7 colunas: _Indicador | Definição | Numerador | Denominador | Unidade/escala | Periodicidade | Fonte_; 5–8 linhas do MVP.
- **Figura 2 (Linhagem):** nó do indicador (p.ex., “Mortalidade 2024”) ligado à(s) tabela(s) de fato (deaths/population) e, abaixo, aos arquivos fonte (SIM_2024.xlsx, IBGE_pop_2024.csv) com **fonte/período/versão/hash**.
- **Figura 3 (Fluxo ETL):** swimlanes/fluxograma com **duração média** por etapa (ex.: Ingestão 1–2 min; Normalização 3–5 min; Materialização 1 min; Publicação 30 s).

---

## 13) Anexos úteis
- **Agents.md** — visão geral e diretrizes (estrutura, segurança, convenções).
- **implementacao-backend.md** — tudo que já foi entregue (DW/Stage, serviços, rotas).
- **implementacao-frontend.md** — o que será implementado (páginas, exportação, testes).
