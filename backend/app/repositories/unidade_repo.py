from typing import List, Optional

from sqlmodel import select
from sqlmodel import Session

from app.models.dw import DimUnidade
from app.models.dev_lite import DevDimUnidade


class UnidadeRepository:
    def _model(self, session: Session):
        dialect = session.get_bind().dialect.name if session.get_bind() else ""
        return DevDimUnidade if dialect == "sqlite" else DimUnidade

    def list(self, session: Session, limit: int = 50, offset: int = 0, uf: Optional[str] = None) -> List:
        try:
            Model = self._model(session)
            stmt = select(Model).offset(offset).limit(limit)
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
        cnes: str,
        nome: str,
        tipo_estabelecimento: Optional[str],
        bairro: Optional[str],
        territorio_id: Optional[int],
        gestao: Optional[str],
    ):
        Model = self._model(session)
        dup = session.exec(select(Model).where(Model.cnes == cnes)).first()
        if dup:
            raise ValueError("cnes already exists")
        row = Model(
            cnes=cnes,
            nome=nome,
            tipo_estabelecimento=tipo_estabelecimento,
            bairro=bairro,
            territorio_id=territorio_id,
            gestao=gestao,
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
        cnes: Optional[str] = None,
        nome: Optional[str] = None,
        tipo_estabelecimento: Optional[str] = None,
        bairro: Optional[str] = None,
        territorio_id: Optional[int] = None,
        gestao: Optional[str] = None,
    ):
        Model = self._model(session)
        row = session.get(Model, id_)
        if not row:
            return None
        if cnes and cnes != row.cnes:
            dup = session.exec(select(Model).where(Model.cnes == cnes)).first()
            if dup:
                raise ValueError("cnes already exists")
            row.cnes = cnes
        if nome is not None:
            row.nome = nome
        if tipo_estabelecimento is not None:
            row.tipo_estabelecimento = tipo_estabelecimento
        if bairro is not None:
            row.bairro = bairro
        if territorio_id is not None:
            row.territorio_id = territorio_id
        if gestao is not None:
            row.gestao = gestao
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
