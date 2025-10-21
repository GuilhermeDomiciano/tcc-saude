from typing import List, Optional

from sqlmodel import Session

from app.repositories.fonte_repo import FonteRepository
from app.schemas.fonte import DimFonteRecursoOut, DimFonteRecursoCreate, DimFonteRecursoUpdate


class FonteService:
    def __init__(self, repo: FonteRepository | None = None):
        self.repo = repo or FonteRepository()

    def list(self, session: Session, limit: int = 50, offset: int = 0, codigo: Optional[str] = None) -> List[DimFonteRecursoOut]:
        rows = self.repo.list(session, limit=limit, offset=offset, codigo=codigo)
        return [
            DimFonteRecursoOut(id=r.id, codigo=r.codigo, descricao=r.descricao)
            for r in rows
        ]

    def get(self, session: Session, id_: int) -> Optional[DimFonteRecursoOut]:
        r = self.repo.get(session, id_)
        if not r:
            return None
        return DimFonteRecursoOut(id=r.id, codigo=r.codigo, descricao=r.descricao)

    def create(self, session: Session, payload: DimFonteRecursoCreate) -> DimFonteRecursoOut:
        row = self.repo.create(session, codigo=payload.codigo.strip(), descricao=payload.descricao.strip())
        return DimFonteRecursoOut(id=row.id, codigo=row.codigo, descricao=row.descricao)

    def update(self, session: Session, id_: int, payload: DimFonteRecursoUpdate) -> Optional[DimFonteRecursoOut]:
        row = self.repo.update(
            session,
            id_,
            codigo=payload.codigo.strip() if payload.codigo else None,
            descricao=payload.descricao.strip() if payload.descricao else None,
        )
        if not row:
            return None
        return DimFonteRecursoOut(id=row.id, codigo=row.codigo, descricao=row.descricao)

    def delete(self, session: Session, id_: int) -> bool:
        return self.repo.delete(session, id_)
