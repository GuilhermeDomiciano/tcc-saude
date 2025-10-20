# Pasta `schemas`

Modelos Pydantic (DTOs) para requests/responses. Independentes do ORM.

Exemplo
```python
# app/schemas/report.py
from pydantic import BaseModel

class ReportIn(BaseModel):
    name: str

class ReportOut(BaseModel):
    id: int
    name: str
```
