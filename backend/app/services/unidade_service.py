from typing import List, Optional

from sqlmodel import Session

from app.repositories.unidade_repo import UnidadeRepository
from app.schemas.unidade import DimUnidadeOut


class UnidadeService:
    def __init__(self, repo: UnidadeRepository | None = None):
        self.repo = repo or UnidadeRepository()

    def list(self, session: Session, limit: int = 50, offset: int = 0, uf: Optional[str] = None) -> List[DimUnidadeOut]:
        rows = self.repo.list(session, limit=limit, offset=offset, uf=uf)
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

