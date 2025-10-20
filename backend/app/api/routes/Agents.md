# Pasta `api/routes`

Rotas organizadas por domínio. Cada arquivo define um `APIRouter` e expõe endpoints específicos.

Dica
- Deixe handlers finos e chame `services` p/ regra.

Exemplo
```python
from fastapi import APIRouter, Depends
router = APIRouter(prefix="/reports")

@router.get("")
def list_reports():
    return []
```
