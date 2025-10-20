# Pasta `repositories`

Abstrações de acesso a dados (queries e persistência). Encapsule o ORM/driver aqui.

Exemplo
```python
# app/repositories/report_repo.py
from typing import Protocol

class ReportRepo(Protocol):
    def create(self, name: str) -> int: ...

class InMemoryReportRepo:
    def __init__(self):
        self._db: dict[int, str] = {}
        self._auto = 1
    def create(self, name: str) -> int:
        pk = self._auto; self._auto += 1
        self._db[pk] = name
        return pk
```
