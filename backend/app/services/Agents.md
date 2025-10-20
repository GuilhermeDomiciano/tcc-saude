# Pasta `services`

Regras de negócio e integrações (ex.: storage, fila). Deve ser agnóstica de HTTP/ORM.

Exemplo
```python
# app/services/report_service.py
from app.schemas.report import ReportIn, ReportOut

def create_report(data: ReportIn) -> ReportOut:
    # regra de negócio mínima
    return ReportOut(id=1, name=data.name)
```
