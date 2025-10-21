from typing import List, Optional

from sqlmodel import select, Session

from app.models.dw import DimFonteRecurso; from app.models.dev_lite import DevDimFonteRecurso


class FonteRepository:
    def _model(self, session: Session):
        dialect = session.get_bind().dialect.name if session.get_bind() else ''
        return DevDimFonteRecurso if dialect == 'sqlite' else DimFonteRecurso
    def list(self, session: Session, limit: int = 50, offset: int = 0, codigo: Optional[str] = None) -> List:
        try:
            Model = self._model(session)
            stmt = select(Model)
            if codigo:
                like = f"{codigo}%"
                stmt = stmt.where(DimFonteRecurso.codigo.like(like))
            stmt = stmt.offset(offset).limit(limit)
            return list(session.exec(stmt))
        except Exception:
            return []

    def get(self, session: Session, id_: int):
        try:
            return session.get(Model, id_)
        except Exception:
            return None

    def create(self, session: Session, *, codigo: str, descricao: str):
        dup = session.exec(select(Model).where(DimFonteRecurso.codigo == codigo)).first()
        if dup:
            raise ValueError("codigo already exists")
        row = Model(codigo=codigo, descricao=descricao)
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    def update(self, session: Session, id_: int, *, codigo: Optional[str] = None, descricao: Optional[str] = None):
        row = session.get(Model, id_)
        if not row:
            return None
        if codigo and codigo != row.codigo:
            dup = session.exec(select(Model).where(DimFonteRecurso.codigo == codigo)).first()
            if dup:
                raise ValueError("codigo already exists")
            row.codigo = codigo
        if descricao is not None:
            row.descricao = descricao
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    def delete(self, session: Session, id_: int) -> bool:
        row = session.get(Model, id_)
        if not row:
            return False
        session.delete(row)
        session.commit()
        return True
    
