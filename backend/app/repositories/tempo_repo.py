from typing import List, Optional

from sqlmodel import select
from sqlmodel import Session

from app.models.dw import DimTempo
from app.models.dev_lite import DevDimTempo


class TempoRepository:
    def list(self, session: Session, limit: int = 50, offset: int = 0, ano: Optional[int] = None, mes: Optional[int] = None) -> List:
        try:
            dialect = session.get_bind().dialect.name if session.get_bind() else ""
            Model = DevDimTempo if dialect == "sqlite" else DimTempo
            stmt = select(Model)
            # Filters are placeholders; for dev sqlite we keep it simple
            if ano is not None:
                # Best-effort filter; may be ignored in dev if column absent
                stmt = stmt.where(Model.ano == ano)
            if mes is not None:
                stmt = stmt.where(Model.mes == mes)
            stmt = stmt.offset(offset).limit(limit)
            return list(session.exec(stmt))
        except Exception:
            return []

