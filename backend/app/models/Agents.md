# Pasta `models`

Modelos de persistência (ex.: SQLModel/ORM). Mapeiam tabelas e relações do banco. Não colocar regra de negócio aqui.

Exemplo
```python
# app/models/report.py
#from sqlmodel import SQLModel, Field
#class Report(SQLModel, table=True):
#    id: int | None = Field(default=None, primary_key=True)
#    name: str
```
