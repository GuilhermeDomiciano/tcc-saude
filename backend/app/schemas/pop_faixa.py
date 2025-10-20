from pydantic import BaseModel, Field
from typing import Optional, Literal


SexoLiteral = Literal["M", "F"]


class DimPopFaixaEtariaCreate(BaseModel):
    territorio_id: int
    ano: int
    faixa_etaria: str
    sexo: SexoLiteral
    populacao: int = Field(ge=0)


class DimPopFaixaEtariaUpdate(BaseModel):
    territorio_id: Optional[int] = None
    ano: Optional[int] = None
    faixa_etaria: Optional[str] = None
    sexo: Optional[SexoLiteral] = None
    populacao: Optional[int] = Field(default=None, ge=0)


class DimPopFaixaEtariaOut(BaseModel):
    id: int
    territorio_id: int
    ano: int
    faixa_etaria: str
    sexo: SexoLiteral
    populacao: int

