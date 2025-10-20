from pydantic import BaseModel
from typing import Optional


class FatoCoberturaAPSOut(BaseModel):
    id: int
    data: str
    territorio_id: int
    tipo_equipe: Optional[str] = None
    cobertura_percentual: Optional[float] = None

