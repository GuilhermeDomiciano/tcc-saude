from typing import List, Optional
from datetime import date

from sqlmodel import Session

from app.repositories.tempo_repo import TempoRepository
from app.schemas.tempo import DimTempoOut, DimTempoCreate, DimTempoUpdate


class TempoService:
    def __init__(self, repo: TempoRepository | None = None):
        self.repo = repo or TempoRepository()

    def _parse_date(self, s: str) -> date:
        try:
            return date.fromisoformat(s)
        except Exception as e:
            raise ValueError("data inválida (YYYY-MM-DD)") from e

    def list(self, session: Session, limit: int = 50, offset: int = 0, ano: Optional[int] = None, mes: Optional[int] = None) -> List[DimTempoOut]:
        rows = self.repo.list(session, limit=limit, offset=offset, ano=ano, mes=mes)
        return [
            DimTempoOut(
                id=r.id,
                data=str(getattr(r, "data", "")),
                ano=getattr(r, "ano", 0),
                mes=getattr(r, "mes", 0),
                trimestre=getattr(r, "trimestre", 0),
                quadrimestre=getattr(r, "quadrimestre", 0),
                mes_nome=getattr(r, "mes_nome", None),
            )
            for r in rows
        ]

    def get(self, session: Session, id_: int) -> Optional[DimTempoOut]:
        r = self.repo.get(session, id_)
        if not r:
            return None
        return DimTempoOut(
            id=r.id,
            data=str(getattr(r, "data", "")),
            ano=getattr(r, "ano", 0),
            mes=getattr(r, "mes", 0),
            trimestre=getattr(r, "trimestre", 0),
            quadrimestre=getattr(r, "quadrimestre", 0),
            mes_nome=getattr(r, "mes_nome", None),
        )

    def create(self, session: Session, payload: DimTempoCreate) -> DimTempoOut:
        d = self._parse_date(payload.data)
        row = self.repo.create(
            session,
            data=d,
            ano=payload.ano,
            mes=payload.mes,
            trimestre=payload.trimestre,
            quadrimestre=payload.quadrimestre,
            mes_nome=payload.mes_nome,
        )
        return DimTempoOut(
            id=row.id,
            data=str(row.data),
            ano=row.ano,
            mes=row.mes,
            trimestre=row.trimestre,
            quadrimestre=row.quadrimestre,
            mes_nome=row.mes_nome,
        )

    def update(self, session: Session, id_: int, payload: DimTempoUpdate) -> Optional[DimTempoOut]:
        d = self._parse_date(payload.data) if payload.data else None
        row = self.repo.update(
            session,
            id_,
            data=d,
            ano=payload.ano,
            mes=payload.mes,
            trimestre=payload.trimestre,
            quadrimestre=payload.quadrimestre,
            mes_nome=payload.mes_nome,
        )
        if not row:
            return None
        return DimTempoOut(
            id=row.id,
            data=str(row.data),
            ano=row.ano,
            mes=row.mes,
            trimestre=row.trimestre,
            quadrimestre=row.quadrimestre,
            mes_nome=row.mes_nome,
        )

    def delete(self, session: Session, id_: int) -> bool:
        return self.repo.delete(session, id_)
