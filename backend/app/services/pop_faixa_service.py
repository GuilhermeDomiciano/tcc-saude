from typing import List, Optional

from sqlmodel import Session

from app.repositories.pop_faixa_repo import PopFaixaRepository
from app.schemas.pop_faixa import (
    DimPopFaixaEtariaOut,
    DimPopFaixaEtariaCreate,
    DimPopFaixaEtariaUpdate,
)


class PopFaixaService:
    def __init__(self, repo: PopFaixaRepository | None = None):
        self.repo = repo or PopFaixaRepository()

    def list(
        self,
        session: Session,
        limit: int = 50,
        offset: int = 0,
        territorio_id: Optional[int] = None,
        ano: Optional[int] = None,
    ) -> List[DimPopFaixaEtariaOut]:
        rows = self.repo.list(session, limit=limit, offset=offset, territorio_id=territorio_id, ano=ano)
        return [
            DimPopFaixaEtariaOut(
                id=r.id,
                territorio_id=r.territorio_id,
                ano=r.ano,
                faixa_etaria=r.faixa_etaria,
                sexo=r.sexo,
                populacao=r.populacao,
            )
            for r in rows
        ]

    def get(self, session: Session, id_: int) -> Optional[DimPopFaixaEtariaOut]:
        r = self.repo.get(session, id_)
        if not r:
            return None
        return DimPopFaixaEtariaOut(
            id=r.id,
            territorio_id=r.territorio_id,
            ano=r.ano,
            faixa_etaria=r.faixa_etaria,
            sexo=r.sexo,
            populacao=r.populacao,
        )

    def create(self, session: Session, payload: DimPopFaixaEtariaCreate) -> DimPopFaixaEtariaOut:
        row = self.repo.create(
            session,
            territorio_id=payload.territorio_id,
            ano=payload.ano,
            faixa_etaria=payload.faixa_etaria.strip(),
            sexo=payload.sexo,
            populacao=payload.populacao,
        )
        return DimPopFaixaEtariaOut(
            id=row.id,
            territorio_id=row.territorio_id,
            ano=row.ano,
            faixa_etaria=row.faixa_etaria,
            sexo=row.sexo,
            populacao=row.populacao,
        )

    def update(self, session: Session, id_: int, payload: DimPopFaixaEtariaUpdate) -> Optional[DimPopFaixaEtariaOut]:
        row = self.repo.update(
            session,
            id_,
            territorio_id=payload.territorio_id,
            ano=payload.ano,
            faixa_etaria=payload.faixa_etaria.strip() if payload.faixa_etaria else None,
            sexo=payload.sexo,
            populacao=payload.populacao,
        )
        if not row:
            return None
        return DimPopFaixaEtariaOut(
            id=row.id,
            territorio_id=row.territorio_id,
            ano=row.ano,
            faixa_etaria=row.faixa_etaria,
            sexo=row.sexo,
            populacao=row.populacao,
        )

    def delete(self, session: Session, id_: int) -> bool:
        return self.repo.delete(session, id_)

