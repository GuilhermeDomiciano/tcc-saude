from typing import List, Optional

from sqlmodel import Session

from app.repositories.equipe_repo import EquipeRepository
from app.schemas.equipe import DimEquipeOut, DimEquipeCreate, DimEquipeUpdate


class EquipeService:
    def __init__(self, repo: EquipeRepository | None = None):
        self.repo = repo or EquipeRepository()

    def list(self, session: Session, limit: int = 50, offset: int = 0) -> List[DimEquipeOut]:
        rows = self.repo.list(session, limit=limit, offset=offset)
        return [
            DimEquipeOut(
                id=r.id,
                id_equipe=r.id_equipe,
                tipo=r.tipo,
                unidade_id=getattr(r, "unidade_id", None),
                territorio_id=getattr(r, "territorio_id", None),
                ativo=getattr(r, "ativo", True),
            )
            for r in rows
        ]

    def get(self, session: Session, id_: int) -> Optional[DimEquipeOut]:
        r = self.repo.get(session, id_)
        if not r:
            return None
        return DimEquipeOut(
            id=r.id,
            id_equipe=r.id_equipe,
            tipo=r.tipo,
            unidade_id=getattr(r, "unidade_id", None),
            territorio_id=getattr(r, "territorio_id", None),
            ativo=getattr(r, "ativo", True),
        )

    def create(self, session: Session, payload: DimEquipeCreate) -> DimEquipeOut:
        row = self.repo.create(
            session,
            id_equipe=payload.id_equipe.strip(),
            tipo=payload.tipo,
            unidade_id=payload.unidade_id,
            territorio_id=payload.territorio_id,
            ativo=payload.ativo,
        )
        return DimEquipeOut(
            id=row.id,
            id_equipe=row.id_equipe,
            tipo=row.tipo,
            unidade_id=getattr(row, "unidade_id", None),
            territorio_id=getattr(row, "territorio_id", None),
            ativo=getattr(row, "ativo", True),
        )

    def update(self, session: Session, id_: int, payload: DimEquipeUpdate) -> Optional[DimEquipeOut]:
        row = self.repo.update(
            session,
            id_,
            id_equipe=payload.id_equipe.strip() if payload.id_equipe else None,
            tipo=payload.tipo,
            unidade_id=payload.unidade_id,
            territorio_id=payload.territorio_id,
            ativo=payload.ativo,
        )
        if not row:
            return None
        return DimEquipeOut(
            id=row.id,
            id_equipe=row.id_equipe,
            tipo=row.tipo,
            unidade_id=getattr(row, "unidade_id", None),
            territorio_id=getattr(row, "territorio_id", None),
            ativo=getattr(row, "ativo", True),
        )

    def delete(self, session: Session, id_: int) -> bool:
        return self.repo.delete(session, id_)

