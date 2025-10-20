# Guia da pasta `app`

Esta pasta contém o código-fonte da API, organizado por camadas (core, api, models, schemas, services, repositories, utils, workers). Use cada subpasta para sua responsabilidade específica.

- core: configuração e inicialização.
- api: rotas HTTP (FastAPI) e dependências.
- models: modelos de persistência (ex.: SQLModel/ORM).
- schemas: modelos Pydantic para requests/responses.
- services: regras de negócio e integrações externas.
- repositories: acesso a dados (queries, persistência).
- utils: utilitários pequenos.
- workers: jobs/tarefas assíncronas.

Exemplo
- Adicionar uma nova feature “reports” criando:
  - `schemas/report.py` (DTOs), `services/report_service.py` (regra), `repositories/report_repo.py` (dados), `api/routes/reports.py` (rotas).
