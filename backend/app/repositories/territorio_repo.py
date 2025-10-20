from typing import List

from sqlmodel import select
from sqlmodel import Session

from app.models.dw import DimTerritorio
from app.models.dev_lite import DevDimTerritorio


class TerritorioRepository:
    def list(self, session: Session, limit: int = 50, offset: int = 0) -> List[DimTerritorio]:
        try:
            dialect = session.get_bind().dialect.name if session.get_bind() else ""
            Model = DevDimTerritorio if dialect == "sqlite" else DimTerritorio
            stmt = select(Model).offset(offset).limit(limit)
            return list(session.exec(stmt))
        except Exception:
            return []
