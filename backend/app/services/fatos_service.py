from datetime import date
from typing import List, Optional

from sqlmodel import Session

from app.repositories.fatos_repo import FatosRepository
from app.schemas.fatos import FatoCoberturaAPSOut


class FatosService:
    def __init__(self, repo: FatosRepository | None = None):
        self.repo = repo or FatosRepository()

    def list_cobertura(
        self,
        session: Session,
        limit: int = 50,
        offset: int = 0,
        data_ini: Optional[date] = None,
        data_fim: Optional[date] = None,
        territorio_id: Optional[int] = None,
    ) -> List[FatoCoberturaAPSOut]:
        rows = self.repo.list_cobertura(
            session,
            limit=limit,
            offset=offset,
            data_ini=data_ini,
            data_fim=data_fim,
            territorio_id=territorio_id,
        )
        return [
            FatoCoberturaAPSOut(
                id=r.id,
                data=str(getattr(r, "data", "")),
                territorio_id=getattr(r, "territorio_id", 0),
                tipo_equipe=getattr(r, "tipo_equipe", None),
                cobertura_percentual=getattr(r, "cobertura_percentual", None),
            )
            for r in rows
        ]

