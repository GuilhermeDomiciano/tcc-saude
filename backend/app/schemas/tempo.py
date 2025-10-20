from pydantic import BaseModel, Field
from typing import Optional


class DimTempoCreate(BaseModel):
    data: str
    ano: int
    mes: int = Field(ge=1, le=12)
    trimestre: int = Field(ge=1, le=4)
    quadrimestre: int = Field(ge=1, le=3)
    mes_nome: Optional[str] = None


class DimTempoUpdate(BaseModel):
    data: Optional[str] = None
    ano: Optional[int] = None
    mes: Optional[int] = Field(default=None, ge=1, le=12)
    trimestre: Optional[int] = Field(default=None, ge=1, le=4)
    quadrimestre: Optional[int] = Field(default=None, ge=1, le=3)
    mes_nome: Optional[str] = None


class DimTempoOut(BaseModel):
    id: int
    data: str
    ano: int
    mes: int
    trimestre: int
    quadrimestre: int
    mes_nome: Optional[str] = None
