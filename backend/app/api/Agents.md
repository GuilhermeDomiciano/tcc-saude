# Pasta `api`

Camada HTTP (FastAPI). Contém roteadores, dependências e validação de entrada/saída. Sem regra de negócio direta — delegue para `services`.

Estrutura
- `__init__.py`: agrega e expõe `api_router`.
- `routes/`: módulos de rotas por domínio.

Exemplo de rota
```python
# app/api/routes/ping.py
from fastapi import APIRouter
router = APIRouter()

@router.get("/ping")
def ping():
    return {"pong": True}
```
```python
# app/api/__init__.py
from fastapi import APIRouter
from .routes.ping import router as ping_router

api_router = APIRouter()
api_router.include_router(ping_router, tags=["ping"]) 
```
