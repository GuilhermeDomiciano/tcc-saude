from fastapi.testclient import TestClient
from backend.main import app
from app.core.db import engine
from sqlmodel import Session, select
from app.models.dev_lite import DevRefIndicador, DevCalcIndicador


client = TestClient(app)


def seed_cobertura(periodo: str = "2025-02"):
    with Session(engine) as session:
        # limpar
        for model in (DevRefIndicador, DevCalcIndicador):
            rows = session.exec(select(model).where(model.periodo == periodo)).all()
            for r in rows:
                session.delete(r)
        session.commit()

        # 3 quadrantes esperados, 2 gerados -> 66.666%
        session.add_all([
            DevRefIndicador(indicador="cov_aps", chave="mun=1", periodo=periodo, valor=100.0),
            DevRefIndicador(indicador="cov_aps", chave="mun=2", periodo=periodo, valor=80.0),
            DevRefIndicador(indicador="cov_aps", chave="mun=3", periodo=periodo, valor=50.0),
        ])
        session.add_all([
            DevCalcIndicador(indicador="cov_aps", chave="mun=1", periodo=periodo, valor=95.0),
            DevCalcIndicador(indicador="cov_aps", chave="mun=2", periodo=periodo, valor=82.0),
        ])
        session.commit()


def test_rdqa_cobertura_percent_and_missing():
    seed_cobertura()
    r = client.get("/rdqa/cobertura", params={"periodo": "2025-02"})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 3
    assert body["gerados"] == 2
    assert abs(body["percent"] - (2/3*100)) < 1e-6
    faltantes = body["faltantes"]
    assert any(it["quadro"].endswith("mun=3") and it["motivo"] == "sem dados" for it in faltantes)

