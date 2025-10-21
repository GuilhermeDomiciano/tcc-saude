from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import JSON
from sqlmodel import Field, SQLModel


class StageBase(SQLModel):
    __table_args__ = {"schema": "stage"}


class RawIngest(StageBase, table=True):
    """Ingestão bruta de arquivos (RDQA/planilhas/etc.) em JSONB.

    Observa o contrato descrito em backend/db/geral.sql.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    fonte: str
    periodo_ref: str
    payload: Dict[str, Any] = Field(sa_type=JSON)
    ingested_at: datetime = Field(default_factory=datetime.utcnow)


__all__ = ["RawIngest"]


class RefIndicador(StageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    indicador: str
    chave: str
    periodo: str
    valor: float


class CalcIndicador(StageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    indicador: str
    chave: str
    periodo: str
    valor: float


__all__ += ["RefIndicador", "CalcIndicador"]
