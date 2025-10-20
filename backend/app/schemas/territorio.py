from pydantic import BaseModel, Field
from typing import Optional


class DimTerritorioCreate(BaseModel):
    cod_ibge_municipio: str = Field(min_length=6, max_length=7)
    nome: str
    uf: str = Field(min_length=2, max_length=2)
    area_km2: Optional[float] = None
    pop_censo_2022: Optional[int] = None
    pop_estim_2024: Optional[int] = None


class DimTerritorioUpdate(BaseModel):
    cod_ibge_municipio: Optional[str] = Field(default=None, min_length=6, max_length=7)
    nome: Optional[str] = None
    uf: Optional[str] = Field(default=None, min_length=2, max_length=2)
    area_km2: Optional[float] = None
    pop_censo_2022: Optional[int] = None
    pop_estim_2024: Optional[int] = None


class DimTerritorioOut(BaseModel):
    id: int
    cod_ibge_municipio: str
    nome: str
    uf: str
    area_km2: Optional[float] = None
    pop_censo_2022: Optional[int] = None
    pop_estim_2024: Optional[int] = None
