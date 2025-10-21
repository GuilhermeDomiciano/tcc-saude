from pydantic import BaseModel, Field
from typing import Optional


class DimTempoCreate(BaseModel):
    data: str
    ano: int
    mes: int = Field(ge=1, le=12)
    trimestre: int = Field(ge=1, le=4)
    quadrimestre: int = Field(ge=1, le=3)
    mes_nome: Optional[str] = None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "data": "2025-01-01",
                    "ano": 2025,
                    "mes": 1,
                    "trimestre": 1,
                    "quadrimestre": 1,
                    "mes_nome": "Janeiro",
                }
            ]
        }
    }


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
    fonte: Optional[str] = None
    periodo: Optional[str] = None
    versao: Optional[str] = None
    hash: Optional[str] = None
    exec_id: Optional[str] = None
