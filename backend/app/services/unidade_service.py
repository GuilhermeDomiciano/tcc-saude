from typing import List, Optional

from sqlmodel import Session

from app.repositories.unidade_repo import UnidadeRepository
from app.schemas.unidade import DimUnidadeOut, DimUnidadeCreate, DimUnidadeUpdate


class UnidadeService:
    def __init__(self, repo: UnidadeRepository | None = None):
        self.repo = repo or UnidadeRepository()

    def list(
        self,
        session: Session,
        limit: int = 50,
        offset: int = 0,
        uf: Optional[str] = None,
        cnes: Optional[str] = None,
        territorio_id: Optional[int] = None,
    ) -> List[DimUnidadeOut]:
        rows = self.repo.list(session, limit=limit, offset=offset, uf=uf, cnes=cnes, territorio_id=territorio_id)
        return [
            DimUnidadeOut(
                id=r.id,
                cnes=r.cnes,
                nome=r.nome,
                tipo_estabelecimento=getattr(r, "tipo_estabelecimento", None),
                bairro=getattr(r, "bairro", None),
                territorio_id=getattr(r, "territorio_id", None),
                gestao=getattr(r, "gestao", None),
            )
            for r in rows
        ]

    def get(self, session: Session, id_: int) -> Optional[DimUnidadeOut]:
        r = self.repo.get(session, id_)
        if not r:
            return None
        return DimUnidadeOut(
            id=r.id,
            cnes=r.cnes,
            nome=r.nome,
            tipo_estabelecimento=getattr(r, "tipo_estabelecimento", None),
            bairro=getattr(r, "bairro", None),
            territorio_id=getattr(r, "territorio_id", None),
            gestao=getattr(r, "gestao", None),
        )

    def create(self, session: Session, payload: DimUnidadeCreate) -> DimUnidadeOut:
        row = self.repo.create(
            session,
            cnes=payload.cnes.strip(),
            nome=payload.nome.strip(),
            tipo_estabelecimento=payload.tipo_estabelecimento,
            bairro=payload.bairro,
            territorio_id=payload.territorio_id,
            gestao=payload.gestao,
        )
        return DimUnidadeOut(
            id=row.id,
            cnes=row.cnes,
            nome=row.nome,
            tipo_estabelecimento=getattr(row, "tipo_estabelecimento", None),
            bairro=getattr(row, "bairro", None),
            territorio_id=getattr(row, "territorio_id", None),
            gestao=getattr(row, "gestao", None),
        )

    def update(self, session: Session, id_: int, payload: DimUnidadeUpdate) -> Optional[DimUnidadeOut]:
        row = self.repo.update(
            session,
            id_,
            cnes=payload.cnes.strip() if payload.cnes else None,
            nome=payload.nome.strip() if payload.nome else None,
            tipo_estabelecimento=payload.tipo_estabelecimento,
            bairro=payload.bairro,
            territorio_id=payload.territorio_id,
            gestao=payload.gestao,
        )
        if not row:
            return None
        return DimUnidadeOut(
            id=row.id,
            cnes=row.cnes,
            nome=row.nome,
            tipo_estabelecimento=getattr(row, "tipo_estabelecimento", None),
            bairro=getattr(row, "bairro", None),
            territorio_id=getattr(row, "territorio_id", None),
            gestao=getattr(row, "gestao", None),
        )

    def delete(self, session: Session, id_: int) -> bool:
        return self.repo.delete(session, id_)
