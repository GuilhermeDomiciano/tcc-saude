from pydantic import BaseModel, Field
from typing import Optional, Literal


EquipeTipoLiteral = Literal["ESF", "ESB", "ACS", "OUTROS"]


class DimEquipeCreate(BaseModel):
    id_equipe: str
    tipo: EquipeTipoLiteral
    unidade_id: Optional[int] = None
    territorio_id: Optional[int] = None
    ativo: bool = True


class DimEquipeUpdate(BaseModel):
    id_equipe: Optional[str] = None
    tipo: Optional[EquipeTipoLiteral] = None
    unidade_id: Optional[int] = None
    territorio_id: Optional[int] = None
    ativo: Optional[bool] = None


class DimEquipeOut(BaseModel):
    id: int
    id_equipe: str
    tipo: EquipeTipoLiteral
    unidade_id: Optional[int] = None
    territorio_id: Optional[int] = None
    ativo: bool
    fonte: Optional[str] = None
    periodo: Optional[str] = None
    versao: Optional[str] = None
    hash: Optional[str] = None
    exec_id: Optional[str] = None
