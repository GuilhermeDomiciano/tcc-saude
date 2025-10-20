from pydantic import BaseModel
from typing import Optional


class DimUnidadeOut(BaseModel):
    id: int
    cnes: str
    nome: str
    tipo_estabelecimento: Optional[str] = None
    bairro: Optional[str] = None
    territorio_id: Optional[int] = None
    gestao: Optional[str] = None

