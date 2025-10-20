from typing import List

from sqlmodel import Session

from app.repositories.territorio_repo import TerritorioRepository
from app.schemas.territorio import DimTerritorioOut


class TerritorioService:
    def __init__(self, repo: TerritorioRepository | None = None):
        self.repo = repo or TerritorioRepository()

    def list(self, session: Session, limit: int = 50, offset: int = 0) -> List[DimTerritorioOut]:
        rows = self.repo.list(session, limit=limit, offset=offset)
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

