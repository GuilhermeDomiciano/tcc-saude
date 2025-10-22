from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class RAGFinanceiroOut(BaseModel):
    territorio_id: int
    territorio_nome: Optional[str] = None
    periodo: str
    dotacao_atualizada: Optional[float] = Field(None, description="Dotação atualizada anual (R$)")
    receita_realizada: Optional[float] = Field(None, description="Receita realizada (R$)")
    empenhado: Optional[float] = Field(None, description="Valor empenhado (R$)")
    liquidado: Optional[float] = Field(None, description="Valor liquidado (R$)")
    pago: Optional[float] = Field(None, description="Valor pago (R$)")


class RAGProducaoOut(BaseModel):
    territorio_id: int
    territorio_nome: Optional[str] = None
    periodo: str
    tipo: str
    quantidade: Optional[int] = None


class RAGMetaOut(BaseModel):
    territorio_id: int
    territorio_nome: Optional[str] = None
    periodo: str
    indicador: str
    meta_planejada: Optional[float] = None
    meta_executada: Optional[float] = None
    cumprida: Optional[bool] = None


class RAGResumoItem(BaseModel):
    territorio_id: int
    territorio_nome: Optional[str] = None
    periodo: str
    dotacao_atualizada: Optional[float] = None
    receita_realizada: Optional[float] = None
    empenhado: Optional[float] = None
    liquidado: Optional[float] = None
    pago: Optional[float] = None
    execucao_percentual: Optional[float] = Field(None, description="Percentual pago / dotação")
    producao_total: Optional[int] = None
    metas_cumpridas: int = 0
    metas_total: int = 0


class RAGResumoOut(BaseModel):
    periodos: List[str]
    itens: List[RAGResumoItem]


class RAGExportIn(BaseModel):
    html: Optional[str] = None
    url: Optional[str] = None
    format: str = "A4"
    margin_mm: int = 12
