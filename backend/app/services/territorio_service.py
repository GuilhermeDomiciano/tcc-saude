from typing import List, Optional

from sqlmodel import Session

from app.repositories.territorio_repo import TerritorioRepository
from app.schemas.territorio import (
    DimTerritorioOut,
    DimTerritorioCreate,
    DimTerritorioUpdate,
)


class TerritorioService:
    def __init__(self, repo: TerritorioRepository | None = None):
        self.repo = repo or TerritorioRepository()

    def _normalize_uf(self, uf: str) -> str:
        return uf.strip().upper()

    def _validate_ibge(self, cod: str) -> None:
        s = cod.strip()
        if len(s) not in (6, 7) or not s.isdigit():
            raise ValueError("cod_ibge_municipio inválido (6-7 dígitos)")

    def list(
        self,
        session: Session,
        limit: int = 50,
        offset: int = 0,
        uf: Optional[str] = None,
        cod_ibge_municipio: Optional[str] = None,
    ) -> List[DimTerritorioOut]:
        rows = self.repo.list(session, limit=limit, offset=offset, uf=uf, cod_ibge_municipio=cod_ibge_municipio)
        return [
            DimTerritorioOut(
                id=r.id,
                cod_ibge_municipio=r.cod_ibge_municipio,
                nome=r.nome,
                uf=r.uf,
                area_km2=r.area_km2,
                pop_censo_2022=r.pop_censo_2022,
                pop_estim_2024=r.pop_estim_2024,
            )
            for r in rows
        ]

    def get(self, session: Session, id_: int) -> Optional[DimTerritorioOut]:
        r = self.repo.get(session, id_)
        if not r:
            return None
        return DimTerritorioOut(
            id=r.id,
            cod_ibge_municipio=r.cod_ibge_municipio,
            nome=r.nome,
            uf=r.uf,
            area_km2=r.area_km2,
            pop_censo_2022=r.pop_censo_2022,
            pop_estim_2024=r.pop_estim_2024,
        )

    def create(self, session: Session, payload: DimTerritorioCreate) -> DimTerritorioOut:
        self._validate_ibge(payload.cod_ibge_municipio)
        uf = self._normalize_uf(payload.uf)
        row = self.repo.create(
            session,
            cod_ibge_municipio=payload.cod_ibge_municipio.strip(),
            nome=payload.nome.strip(),
            uf=uf,
            area_km2=payload.area_km2,
            pop_censo_2022=payload.pop_censo_2022,
            pop_estim_2024=payload.pop_estim_2024,
        )
        return DimTerritorioOut(
            id=row.id,
            cod_ibge_municipio=row.cod_ibge_municipio,
            nome=row.nome,
            uf=row.uf,
            area_km2=row.area_km2,
            pop_censo_2022=row.pop_censo_2022,
            pop_estim_2024=row.pop_estim_2024,
        )

    def update(self, session: Session, id_: int, payload: DimTerritorioUpdate) -> Optional[DimTerritorioOut]:
        cod = payload.cod_ibge_municipio.strip() if payload.cod_ibge_municipio else None
        if cod:
            self._validate_ibge(cod)
        uf = self._normalize_uf(payload.uf) if payload.uf else None
        row = self.repo.update(
            session,
            id_,
            cod_ibge_municipio=cod,
            nome=payload.nome.strip() if payload.nome else None,
            uf=uf,
            area_km2=payload.area_km2,
            pop_censo_2022=payload.pop_censo_2022,
            pop_estim_2024=payload.pop_estim_2024,
        )
        if not row:
            return None
        return DimTerritorioOut(
            id=row.id,
            cod_ibge_municipio=row.cod_ibge_municipio,
            nome=row.nome,
            uf=row.uf,
            area_km2=row.area_km2,
            pop_censo_2022=row.pop_censo_2022,
            pop_estim_2024=row.pop_estim_2024,
        )

    def delete(self, session: Session, id_: int) -> bool:
        return self.repo.delete(session, id_)
