from typing import List, Optional

from sqlmodel import select
from sqlmodel import Session

from app.models.dw import DimTempo
from app.models.dev_lite import DevDimTempo


class TempoRepository:
    def _model(self, session: Session):
        dialect = session.get_bind().dialect.name if session.get_bind() else ""
        return DevDimTempo if dialect == "sqlite" else DimTempo

    def list(self, session: Session, limit: int = 50, offset: int = 0, ano: Optional[int] = None, mes: Optional[int] = None) -> List:
        try:
            Model = self._model(session)
            stmt = select(Model)
            if ano is not None:
                stmt = stmt.where(Model.ano == ano)
            if mes is not None:
                stmt = stmt.where(Model.mes == mes)
            stmt = stmt.offset(offset).limit(limit)
            return list(session.exec(stmt))
        except Exception:
            return []

    def get(self, session: Session, id_: int):
        try:
            Model = self._model(session)
            return session.get(Model, id_)
        except Exception:
            return None

    def create(
        self,
        session: Session,
        *,
        data,
        ano: int,
        mes: int,
        trimestre: int,
        quadrimestre: int,
        mes_nome: Optional[str],
    ):
        Model = self._model(session)
        dup = session.exec(select(Model).where(Model.data == data)).first()
        if dup:
            raise ValueError("data already exists")
        row = Model(
            data=data,
            ano=ano,
            mes=mes,
            trimestre=trimestre,
            quadrimestre=quadrimestre,
            mes_nome=mes_nome,
        )
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    def update(
        self,
        session: Session,
        id_: int,
        *,
        data=None,
        ano: Optional[int] = None,
        mes: Optional[int] = None,
        trimestre: Optional[int] = None,
        quadrimestre: Optional[int] = None,
        mes_nome: Optional[str] = None,
    ):
        Model = self._model(session)
        row = session.get(Model, id_)
        if not row:
            return None
        if data is not None and data != getattr(row, "data", None):
            dup = session.exec(select(Model).where(Model.data == data)).first()
            if dup:
                raise ValueError("data already exists")
            row.data = data
        if ano is not None:
            row.ano = ano
        if mes is not None:
            row.mes = mes
        if trimestre is not None:
            row.trimestre = trimestre
        if quadrimestre is not None:
            row.quadrimestre = quadrimestre
        if mes_nome is not None:
            row.mes_nome = mes_nome
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    def delete(self, session: Session, id_: int) -> bool:
        Model = self._model(session)
        row = session.get(Model, id_)
        if not row:
            return False
        session.delete(row)
        session.commit()
        return True
