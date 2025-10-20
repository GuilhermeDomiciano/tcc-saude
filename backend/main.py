from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api import api_router
from app.core.db import engine
from sqlmodel import SQLModel, Session, select
from app.models.dev_lite import (
    DevDimTerritorio,
    DevDimUnidade,
    DevDimTempo,
    DevDimPopFaixaEtaria,
)
from datetime import date
from pathlib import Path
from sqlalchemy import text as sa_text
import logging
try:
    from alembic.config import Config as AlembicConfig
    from alembic import command as alembic_command
except Exception:  # alembic optional in dev
    AlembicConfig = None
    alembic_command = None


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.allowed_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.core.errors import register_exception_handlers
    register_exception_handlers(app)

    app.include_router(api_router)

    @app.on_event("startup")
    def _startup():
        dialect = engine.dialect.name

        # Production path: ensure schemas and run Alembic (Postgres)
        if dialect in {"postgresql"} and AlembicConfig and alembic_command:
            try:
                with engine.begin() as conn:
                    conn.execute(sa_text("CREATE SCHEMA IF NOT EXISTS dw"))
                    conn.execute(sa_text("CREATE SCHEMA IF NOT EXISTS stage"))
            except Exception as e:
                logging.warning(f"Could not ensure schemas: {e}")
            try:
                cfg = AlembicConfig(str((Path(__file__).parent / "alembic.ini").resolve()))
                cfg.set_main_option("sqlalchemy.url", str(engine.url))
                cfg.set_main_option("script_location", str((Path(__file__).parent / "alembic").resolve()))
                alembic_command.upgrade(cfg, "head")
            except Exception as e:
                logging.error(f"Alembic upgrade failed: {e}")

        # SQLite-dev bootstrap: create tables and seed minimal data if empty
        if dialect == "sqlite":
            SQLModel.metadata.create_all(bind=engine, tables=[
                DevDimTerritorio.__table__,
                DevDimUnidade.__table__,
                DevDimTempo.__table__,
                DevDimPopFaixaEtaria.__table__,
            ])
            with Session(engine) as session:
                try:
                    exists = session.exec(select(DevDimTerritorio).limit(1)).first()
                except Exception:
                    exists = None
                if not exists:
                    session.add_all([
                        DevDimTerritorio(cod_ibge_municipio="4300000", nome="Municipio A", uf="RS"),
                        DevDimTerritorio(cod_ibge_municipio="4200000", nome="Municipio B", uf="SC"),
                    ])
                    session.commit()
                try:
                    exists_u = session.exec(select(DevDimUnidade).limit(1)).first()
                except Exception:
                    exists_u = None
                if not exists_u:
                    session.add_all([
                        DevDimUnidade(cnes="0000001", nome="UBS Central", territorio_id=1, tipo_estabelecimento="UBS", bairro="Centro", gestao="Municipal"),
                        DevDimUnidade(cnes="0000002", nome="USF Norte", territorio_id=2, tipo_estabelecimento="USF", bairro="Norte", gestao="Municipal"),
                    ])
                    session.commit()
                try:
                    exists_t = session.exec(select(DevDimTempo).limit(1)).first()
                except Exception:
                    exists_t = None
                if not exists_t:
                    session.add_all([
                        DevDimTempo(data=date.fromisoformat("2025-01-01"), ano=2025, mes=1, trimestre=1, quadrimestre=1, mes_nome="Janeiro"),
                        DevDimTempo(data=date.fromisoformat("2025-02-01"), ano=2025, mes=2, trimestre=1, quadrimestre=1, mes_nome="Fevereiro"),
                    ])
                    session.commit()
                try:
                    exists_pf = session.exec(select(DevDimPopFaixaEtaria).limit(1)).first()
                except Exception:
                    exists_pf = None
                if not exists_pf:
                    session.add_all([
                        DevDimPopFaixaEtaria(territorio_id=1, ano=2025, faixa_etaria="0-4", sexo="M", populacao=3500),
                        DevDimPopFaixaEtaria(territorio_id=1, ano=2025, faixa_etaria="0-4", sexo="F", populacao=3300),
                        DevDimPopFaixaEtaria(territorio_id=2, ano=2025, faixa_etaria="0-4", sexo="M", populacao=2800),
                        DevDimPopFaixaEtaria(territorio_id=2, ano=2025, faixa_etaria="0-4", sexo="F", populacao=2700),
                    ])
                    session.commit()
    return app


app = create_app()
