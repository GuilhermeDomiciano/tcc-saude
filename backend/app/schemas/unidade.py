from pydantic import BaseModel, Field
from typing import Optional


class DimUnidadeCreate(BaseModel):
    cnes: str = Field(min_length=1, max_length=15)
    nome: str
    tipo_estabelecimento: Optional[str] = None
    bairro: Optional[str] = None
    territorio_id: Optional[int] = None
    gestao: Optional[str] = None


class DimUnidadeUpdate(BaseModel):
    cnes: Optional[str] = Field(default=None, min_length=1, max_length=15)
    nome: Optional[str] = None
    tipo_estabelecimento: Optional[str] = None
    bairro: Optional[str] = None
    territorio_id: Optional[int] = None
    gestao: Optional[str] = None


class DimUnidadeOut(BaseModel):
    id: int
    cnes: str
    nome: str
    tipo_estabelecimento: Optional[str] = None
    bairro: Optional[str] = None
    territorio_id: Optional[int] = None
    gestao: Optional[str] = None
    fonte: Optional[str] = None
    periodo: Optional[str] = None
    versao: Optional[str] = None
    hash: Optional[str] = None
    exec_id: Optional[str] = None
