from typing import List, Optional

from sqlmodel import select
from sqlmodel import Session

from app.models.dw import DimUnidade
from app.models.dev_lite import DevDimUnidade


class UnidadeRepository:
    def list(self, session: Session, limit: int = 50, offset: int = 0, uf: Optional[str] = None) -> List:
        try:
            dialect = session.get_bind().dialect.name if session.get_bind() else ""
            Model = DevDimUnidade if dialect == "sqlite" else DimUnidade
            stmt = select(Model).offset(offset).limit(limit)
            # If using real schema, could join by territorio to filter by UF; in dev, filter not applied
            return list(session.exec(stmt))
        except Exception:
            return []

