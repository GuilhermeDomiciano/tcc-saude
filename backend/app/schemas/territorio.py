from pydantic import BaseModel
from typing import Optional


class DimTerritorioOut(BaseModel):
    id: int
    cod_ibge_municipio: str
    nome: str
    uf: str
    area_km2: Optional[float] = None
    pop_censo_2022: Optional[int] = None
    pop_estim_2024: Optional[int] = None

