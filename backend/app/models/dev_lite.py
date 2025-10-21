from __future__ import annotations

from typing import Optional
from datetime import date
from sqlmodel import Field, SQLModel


class DevDimTerritorio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cod_ibge_municipio: str
    nome: str
    uf: str
    area_km2: Optional[float] = None
    pop_censo_2022: Optional[int] = None
    pop_estim_2024: Optional[int] = None


class DevDimUnidade(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cnes: str
    nome: str
    tipo_estabelecimento: Optional[str] = None
    bairro: Optional[str] = None
    territorio_id: Optional[int] = None
    gestao: Optional[str] = None


class DevDimTempo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: date
    ano: int
    mes: int
    trimestre: int
    quadrimestre: int
    mes_nome: Optional[str] = None

class DevFatoCoberturaAPS(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: date
    tempo_id: int
    territorio_id: int
    equipe_id: Optional[int] = None
    tipo_equipe: Optional[str] = None
    cobertura_percentual: Optional[float] = None


class DevDimPopFaixaEtaria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    territorio_id: int
    ano: int
    faixa_etaria: str
    sexo: str  # 'M' | 'F'
    populacao: int

class DevDimFonteRecurso(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: str
    descricao: str


class DevDimEquipe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_equipe: str
    tipo: Optional[str] = None  # ESF/ESB/ACS/OUTROS
    unidade_id: Optional[int] = None
    territorio_id: Optional[int] = None
    ativo: bool = True
