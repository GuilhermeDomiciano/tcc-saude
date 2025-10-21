from __future__ import annotations

from typing import Optional
from datetime import date, datetime
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


class DevArtefatoExecucao(SQLModel, table=True):
    id: str = Field(primary_key=True)  # exec_id (UUID string)
    hash_sha256: str
    tipo: str = Field(default="rdqa_pdf")
    fonte: Optional[str] = None
    periodo: Optional[str] = None
    versao: Optional[str] = None
    autor: Optional[str] = None
    metadados: Optional[str] = None  # JSON (string) para simplicidade no dev-lite
    ok: bool = True
    mensagem: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DevRefIndicador(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    indicador: str
    chave: str  # dimensão/escopo (ex.: municipio=4300000; equipe=123)
    periodo: str  # ex.: 2025-01, 2025Q1
    valor: float


class DevCalcIndicador(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    indicador: str
    chave: str
    periodo: str
    valor: float
