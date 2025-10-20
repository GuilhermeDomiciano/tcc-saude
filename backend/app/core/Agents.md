# Pasta `core`

Responsável por configuração, inicialização e componentes transversais (ex.: CORS, settings).

Conteúdo comum
- `config.py`: carrega variáveis de ambiente e expõe `Settings`.
- Middlewares/glue do app futuramente.

Exemplo de uso
```python
# app/core/config.py
from dataclasses import dataclass
import os

@dataclass
class Settings:
    app_name: str = "Saúde API"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()
```
```python
# main.py
from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.app_name)
```
