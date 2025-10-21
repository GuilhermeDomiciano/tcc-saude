from typing import List, Optional

from sqlmodel import select, Session

from app.models.dw import DimEquipe


class EquipeRepository:
    def list(self, session: Session, limit: int = 50, offset: int = 0, tipo: Optional[str] = None, ativo: Optional[bool] = None) -> List:
        try:
            stmt = select(DimEquipe)
            if tipo:
                stmt = stmt.where(DimEquipe.tipo == tipo)
                if ativo is not None:
                    stmt = stmt.where(DimEquipe.ativo == ativo)
                    stmt = stmt.offset(offset).limit(limit)
            return list(session.exec(stmt))
        except Exception:
            return []

    def get(self, session: Session, id_: int):
        try:
            return session.get(DimEquipe, id_)
        except Exception:
            return None

    def create(
        self,
        session: Session,
        *,
        id_equipe: str,
        tipo: str,
        unidade_id: Optional[int],
        territorio_id: Optional[int],
        ativo: bool,
    ):
        dup = session.exec(select(DimEquipe).where(DimEquipe.id_equipe == id_equipe)).first()
        if dup:
            raise ValueError("id_equipe already exists")
        row = DimEquipe(
            id_equipe=id_equipe,
            tipo=tipo,
            unidade_id=unidade_id,
            territorio_id=territorio_id,
            ativo=ativo,
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
        id_equipe: Optional[str] = None,
        tipo: Optional[str] = None,
        unidade_id: Optional[int] = None,
        territorio_id: Optional[int] = None,
        ativo: Optional[bool] = None,
    ):
        row = session.get(DimEquipe, id_)
        if not row:
            return None
        if id_equipe and id_equipe != row.id_equipe:
            dup = session.exec(select(DimEquipe).where(DimEquipe.id_equipe == id_equipe)).first()
            if dup:
                raise ValueError("id_equipe already exists")
            row.id_equipe = id_equipe
        if tipo is not None:
            row.tipo = tipo
        if unidade_id is not None:
            row.unidade_id = unidade_id
        if territorio_id is not None:
            row.territorio_id = territorio_id
        if ativo is not None:
            row.ativo = ativo
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    def delete(self, session: Session, id_: int) -> bool:
        row = session.get(DimEquipe, id_)
        if not row:
            return False
        session.delete(row)
        session.commit()
        return True


