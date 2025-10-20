from pydantic import BaseModel
from typing import Optional


class DimTempoOut(BaseModel):
    id: int
    data: str
    ano: int
    mes: int
    trimestre: int
    quadrimestre: int
    mes_nome: Optional[str] = None

