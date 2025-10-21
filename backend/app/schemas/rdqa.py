from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ConsistenciaResumoOut(BaseModel):
    indicador: str
    periodo: Optional[str] = None
    mape: Optional[float] = Field(None, description="Erro Percentual Absoluto Médio (0-100)")
    pares: int


class ConsistenciaDetalheOut(BaseModel):
    indicador: str
    chave: str
    periodo: str
    ref: float
    calc: Optional[float] = None
    erro_abs: Optional[float] = None
    erro_pct: Optional[float] = None


class CoberturaFaltanteItem(BaseModel):
    quadro: str
    periodo: str
    motivo: str


class CoberturaOut(BaseModel):
    percent: float
    total: int
    gerados: int
    faltantes: List[CoberturaFaltanteItem]


class DiffRowOut(BaseModel):
    indicador: str
    chave: str
    periodo_atual: str
    periodo_anterior: str
    valor_atual: Optional[float] = None
    valor_anterior: Optional[float] = None
    delta: Optional[float] = None
    tendencia: Literal["melhora", "piora", "igual"]


class VerificacaoOut(BaseModel):
    ok: bool
    exec_id: Optional[str] = None
    hash: Optional[str] = None
    status: str
    tipo: Optional[str] = None
    fonte: Optional[str] = None
    periodo: Optional[str] = None
    versao: Optional[str] = None
    autor: Optional[str] = None
    mensagem: Optional[str] = None
    created_at: Optional[str] = None

