from typing import List, Optional

from sqlmodel import select
from sqlmodel import Session

from app.models.dw import DimTerritorio
from app.models.dev_lite import DevDimTerritorio


class TerritorioRepository:
    def _model(self, session: Session):
        dialect = session.get_bind().dialect.name if session.get_bind() else ""
        return DevDimTerritorio if dialect == "sqlite" else DimTerritorio

    def list(
        self,
        session: Session,
        limit: int = 50,
        offset: int = 0,
        uf: Optional[str] = None,
        cod_ibge_municipio: Optional[str] = None,
    ) -> List:
        try:
            Model = self._model(session)
            stmt = select(Model)
            if uf:
                stmt = stmt.where(Model.uf == uf)
            if cod_ibge_municipio:
                like = f"{cod_ibge_municipio}%"
                stmt = stmt.where(Model.cod_ibge_municipio.like(like))
            stmt = stmt.offset(offset).limit(limit)
            return list(session.exec(stmt))
        except Exception:
            return []

    def get(self, session: Session, id_: int) -> Optional:
        try:
            Model = self._model(session)
            return session.get(Model, id_)
        except Exception:
            return None

    def create(
        self,
        session: Session,
        *,
        cod_ibge_municipio: str,
        nome: str,
        uf: str,
        area_km2: float | None,
        pop_censo_2022: int | None,
        pop_estim_2024: int | None,
    ):
        Model = self._model(session)
        # Unique check: cod_ibge_municipio
        dup = session.exec(select(Model).where(Model.cod_ibge_municipio == cod_ibge_municipio)).first()
        if dup:
            raise ValueError("cod_ibge_municipio already exists")
        row = Model(
            cod_ibge_municipio=cod_ibge_municipio,
            nome=nome,
            uf=uf,
            area_km2=area_km2,
            pop_censo_2022=pop_censo_2022,
            pop_estim_2024=pop_estim_2024,
        )
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    def update(
        self,
        session: Session,
        id_: int,
        *,
        cod_ibge_municipio: Optional[str] = None,
        nome: Optional[str] = None,
        uf: Optional[str] = None,
        area_km2: Optional[float] = None,
        pop_censo_2022: Optional[int] = None,
        pop_estim_2024: Optional[int] = None,
    ) -> Optional:
        Model = self._model(session)
        row = session.get(Model, id_)
        if not row:
            return None
        if cod_ibge_municipio and cod_ibge_municipio != row.cod_ibge_municipio:
            dup = session.exec(select(Model).where(Model.cod_ibge_municipio == cod_ibge_municipio)).first()
            if dup:
                raise ValueError("cod_ibge_municipio already exists")
            row.cod_ibge_municipio = cod_ibge_municipio
        if nome is not None:
            row.nome = nome
        if uf is not None:
            row.uf = uf
        if area_km2 is not None:
            row.area_km2 = area_km2
        if pop_censo_2022 is not None:
            row.pop_censo_2022 = pop_censo_2022
        if pop_estim_2024 is not None:
            row.pop_estim_2024 = pop_estim_2024
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    def delete(self, session: Session, id_: int) -> bool:
        Model = self._model(session)
        row = session.get(Model, id_)
        if not row:
            return False
        session.delete(row)
        session.commit()
        return True
