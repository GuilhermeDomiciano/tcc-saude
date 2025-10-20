from typing import List, Optional

from sqlmodel import Session

from app.repositories.tempo_repo import TempoRepository
from app.schemas.tempo import DimTempoOut


class TempoService:
    def __init__(self, repo: TempoRepository | None = None):
        self.repo = repo or TempoRepository()

    def list(self, session: Session, limit: int = 50, offset: int = 0, ano: Optional[int] = None, mes: Optional[int] = None) -> List[DimTempoOut]:
        rows = self.repo.list(session, limit=limit, offset=offset, ano=ano, mes=mes)
        return [
            DimTempoOut(
                id=r.id,
                data=str(getattr(r, "data", "")),
                ano=getattr(r, "ano", 0),
                mes=getattr(r, "mes", 0),
                trimestre=getattr(r, "trimestre", 0),
                quadrimestre=getattr(r, "quadrimestre", 0),
                mes_nome=getattr(r, "mes_nome", None),
            )
            for r in rows
        ]

