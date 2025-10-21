from typing import List, Optional

from sqlmodel import select, Session

from app.models.dw import DimFonteRecurso


class FonteRepository:
    def list(self, session: Session, limit: int = 50, offset: int = 0, codigo: Optional[str] = None) -> List:
        try:
            stmt = select(DimFonteRecurso)
            if codigo:
                like = f"{codigo}%"
                stmt = stmt.where(DimFonteRecurso.codigo.like(like))
            stmt = stmt.offset(offset).limit(limit)
            return list(session.exec(stmt))
        except Exception:
            return []

    def get(self, session: Session, id_: int):
        try:
            return session.get(DimFonteRecurso, id_)
        except Exception:
            return None

    def create(self, session: Session, *, codigo: str, descricao: str):
        dup = session.exec(select(DimFonteRecurso).where(DimFonteRecurso.codigo == codigo)).first()
        if dup:
            raise ValueError("codigo already exists")
        row = DimFonteRecurso(codigo=codigo, descricao=descricao)
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    def update(self, session: Session, id_: int, *, codigo: Optional[str] = None, descricao: Optional[str] = None):
        row = session.get(DimFonteRecurso, id_)
        if not row:
            return None
        if codigo and codigo != row.codigo:
            dup = session.exec(select(DimFonteRecurso).where(DimFonteRecurso.codigo == codigo)).first()
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
        row = session.get(DimFonteRecurso, id_)
        if not row:
            return False
        session.delete(row)
        session.commit()
        return True
