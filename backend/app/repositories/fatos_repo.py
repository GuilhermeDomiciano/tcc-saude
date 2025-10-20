from datetime import date
from typing import List, Optional

from sqlmodel import select
from sqlmodel import Session

from app.models.dw import FatoCoberturaAPS
from app.models.dev_lite import DevFatoCoberturaAPS


class FatosRepository:
    def list_cobertura(
        self,
        session: Session,
        limit: int = 50,
        offset: int = 0,
        data_ini: Optional[date] = None,
        data_fim: Optional[date] = None,
        territorio_id: Optional[int] = None,
    ) -> List:
        try:
            dialect = session.get_bind().dialect.name if session.get_bind() else ""
            Model = DevFatoCoberturaAPS if dialect == "sqlite" else FatoCoberturaAPS
            stmt = select(Model)
            if data_ini is not None:
                stmt = stmt.where(Model.data >= data_ini)
            if data_fim is not None:
                stmt = stmt.where(Model.data <= data_fim)
            if territorio_id is not None:
                stmt = stmt.where(Model.territorio_id == territorio_id)
            stmt = stmt.offset(offset).limit(limit)
            return list(session.exec(stmt))
        except Exception:
            return []

