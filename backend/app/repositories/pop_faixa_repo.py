from typing import List, Optional

from sqlmodel import select, Session

from app.models.dw import DimPopFaixaEtaria
from app.models.dev_lite import DevDimPopFaixaEtaria


class PopFaixaRepository:
    def _model(self, session: Session):
        dialect = session.get_bind().dialect.name if session.get_bind() else ""
        return DevDimPopFaixaEtaria if dialect == "sqlite" else DimPopFaixaEtaria
    def list(
        self,
        session: Session,
        limit: int = 50,
        offset: int = 0,
        territorio_id: Optional[int] = None,
        ano: Optional[int] = None,
    ) -> List:
        try:
            Model = self._model(session)
            stmt = select(Model)
            if territorio_id is not None:
                stmt = stmt.where(Model.territorio_id == territorio_id)
            if ano is not None:
                stmt = stmt.where(Model.ano == ano)
            stmt = stmt.offset(offset).limit(limit)
            return list(session.exec(stmt))
        except Exception:
            return []

    def get(self, session: Session, id_: int):
        try:
            Model = self._model(session)
            return session.get(Model, id_)
        except Exception:
            return None

    def create(
        self,
        session: Session,
        *,
        territorio_id: int,
        ano: int,
        faixa_etaria: str,
        sexo: str,
        populacao: int,
    ):
        Model = self._model(session)
        dup = session.exec(
            select(Model).where(
                Model.territorio_id == territorio_id,
                Model.ano == ano,
                Model.faixa_etaria == faixa_etaria,
                Model.sexo == sexo,
            )
        ).first()
        if dup:
            raise ValueError("combination already exists")
        row = Model(
            territorio_id=territorio_id,
            ano=ano,
            faixa_etaria=faixa_etaria,
            sexo=sexo,
            populacao=populacao,
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
        territorio_id: Optional[int] = None,
        ano: Optional[int] = None,
        faixa_etaria: Optional[str] = None,
        sexo: Optional[str] = None,
        populacao: Optional[int] = None,
    ):
        Model = self._model(session)
        row = session.get(Model, id_)
        if not row:
            return None
        # If any component of the unique key changes, validate uniqueness
        new_territorio = territorio_id if territorio_id is not None else row.territorio_id
        new_ano = ano if ano is not None else row.ano
        new_faixa = faixa_etaria if faixa_etaria is not None else row.faixa_etaria
        new_sexo = sexo if sexo is not None else row.sexo
        if (
            new_territorio != row.territorio_id or new_ano != row.ano or new_faixa != row.faixa_etaria or new_sexo != row.sexo
        ):
            dup = session.exec(
                select(Model).where(
                    Model.territorio_id == new_territorio,
                    Model.ano == new_ano,
                    Model.faixa_etaria == new_faixa,
                    Model.sexo == new_sexo,
                )
            ).first()
            if dup:
                raise ValueError("combination already exists")
        if territorio_id is not None:
            row.territorio_id = territorio_id
        if ano is not None:
            row.ano = ano
        if faixa_etaria is not None:
            row.faixa_etaria = faixa_etaria
        if sexo is not None:
            row.sexo = sexo
        if populacao is not None:
            row.populacao = populacao
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
