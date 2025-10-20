# Pasta `utils`

Funções pequenas e utilitárias, sem dependências cíclicas.

Exemplo
```python
# app/utils/time.py
from datetime import datetime, timezone

def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
```
