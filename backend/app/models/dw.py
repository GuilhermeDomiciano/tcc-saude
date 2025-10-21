from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class EquipeTipo(str, Enum):
    ESF = "ESF"
    ESB = "ESB"
    ACS = "ACS"
    OUTROS = "OUTROS"


class Sexo(str, Enum):
    M = "M"
    F = "F"


class DWBase(SQLModel):
    __table_args__ = {"schema": "dw"}


class DemoItem(DWBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    valor: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DimTerritorio(DWBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cod_ibge_municipio: str
    nome: str
    uf: str
    area_km2: Optional[float] = None
    pop_censo_2022: Optional[int] = None
    pop_estim_2024: Optional[int] = None


class DimUnidade(DWBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cnes: str
    nome: str
    tipo_estabelecimento: Optional[str] = None
    bairro: Optional[str] = None
    territorio_id: Optional[int] = Field(default=None, foreign_key="dw.dim_territorio.id")
    gestao: Optional[str] = None


class DimEquipe(DWBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_equipe: str
    tipo: EquipeTipo
    unidade_id: Optional[int] = Field(default=None, foreign_key="dw.dim_unidade.id")
    territorio_id: Optional[int] = Field(default=None, foreign_key="dw.dim_territorio.id")
    ativo: bool = True


class DimFonteRecurso(DWBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: str
    descricao: str


class DimPopFaixaEtaria(DWBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    territorio_id: int = Field(foreign_key="dw.dim_territorio.id")
    ano: int
    faixa_etaria: str
    sexo: Sexo
    populacao: int = Field(ge=0)


class DimTempo(DWBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: date
    ano: int
    mes: int = Field(ge=1, le=12)
    trimestre: int = Field(ge=1, le=4)
    quadrimestre: int = Field(ge=1, le=3)
    mes_nome: Optional[str] = None


class FatoCoberturaAPS(DWBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: date
    tempo_id: int = Field(foreign_key="dw.dim_tempo.id")
    territorio_id: int = Field(foreign_key="dw.dim_territorio.id")
    equipe_id: Optional[int] = Field(default=None, foreign_key="dw.dim_equipe.id")
    tipo_equipe: EquipeTipo
    cobertura_percentual: float = Field(ge=0, le=100)
    pop_coberta_estimada: Optional[int] = Field(default=None, ge=0)
    extract_ts: datetime = Field(default_factory=datetime.utcnow)


class FatoEventosVitais(DWBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: date
    tempo_id: int = Field(foreign_key="dw.dim_tempo.id")
    territorio_id: int = Field(foreign_key="dw.dim_territorio.id")
    nascidos_vivos: int = Field(default=0, ge=0)
    obitos_gerais: Optional[int] = Field(default=None, ge=0)
    fonte: Optional[str] = None
    extract_ts: datetime = Field(default_factory=datetime.utcnow)


class FatoFinancas(DWBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: date
    tempo_id: int = Field(foreign_key="dw.dim_tempo.id")
    territorio_id: int = Field(foreign_key="dw.dim_territorio.id")
    fonte_id: Optional[int] = Field(default=None, foreign_key="dw.dim_fonte_recurso.id")
    dotacao_atualizada_anual: Optional[float] = Field(default=None, ge=0)
    receita_realizada: Optional[float] = Field(default=None, ge=0)
    empenhado: Optional[float] = Field(default=None, ge=0)
    liquidado: Optional[float] = Field(default=None, ge=0)
    pago: Optional[float] = Field(default=None, ge=0)
    extract_ts: datetime = Field(default_factory=datetime.utcnow)


class FatoRedeFisica(DWBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: date
    tempo_id: int = Field(foreign_key="dw.dim_tempo.id")
    territorio_id: int = Field(foreign_key="dw.dim_territorio.id")
    tipo_unidade: str
    quantidade: int = Field(ge=0)
    extract_ts: datetime = Field(default_factory=datetime.utcnow)


class ArtefatoExecucao(DWBase, table=True):
    id: str = Field(primary_key=True)  # exec_id (UUID string)
    hash_sha256: str
    tipo: str = Field(default="rdqa_pdf")
    fonte: Optional[str] = None
    periodo: Optional[str] = None
    versao: Optional[str] = None
    autor: Optional[str] = None
    metadados: Optional[str] = None
    ok: bool = True
    mensagem: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


__all__ = [
    "DemoItem",
    "DimTerritorio",
    "DimUnidade",
    "DimEquipe",
    "DimFonteRecurso",
    "DimPopFaixaEtaria",
    "DimTempo",
    "FatoCoberturaAPS",
    "FatoEventosVitais",
    "FatoFinancas",
    "FatoRedeFisica",
    "ArtefatoExecucao",
    "EquipeTipo",
    "Sexo",
]
