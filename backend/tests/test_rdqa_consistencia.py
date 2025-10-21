from fastapi.testclient import TestClient
from backend.main import app
from app.core.db import engine
from sqlmodel import Session, select
from app.models.dev_lite import DevRefIndicador, DevCalcIndicador


client = TestClient(app)


def seed_indicadores(periodo: str = "2025-01"):
    with Session(engine) as session:
        # limpar entradas anteriores do período/indicador para tornar o teste idempotente
        for model in (DevRefIndicador, DevCalcIndicador):
            rows = session.exec(select(model).where(model.indicador == "cov_aps", model.periodo == periodo)).all()
            for r in rows:
                session.delete(r)
        session.commit()

        session.add_all([
            DevRefIndicador(indicador="cov_aps", chave="mun=1", periodo=periodo, valor=100.0),
            DevRefIndicador(indicador="cov_aps", chave="mun=2", periodo=periodo, valor=50.0),
        ])
        session.add_all([
            DevCalcIndicador(indicador="cov_aps", chave="mun=1", periodo=periodo, valor=110.0),  # 10%
            DevCalcIndicador(indicador="cov_aps", chave="mun=2", periodo=periodo, valor=40.0),   # 20%
        ])
        session.commit()


def test_consistencia_mape_list_and_details():
    seed_indicadores()

    # Listar indicadores (deve incluir cov_aps com MAPE = 15)
    r = client.get("/rdqa/consistencia", params={"periodo": "2025-01"})
    assert r.status_code == 200
    items = r.json()
    row = next((x for x in items if x["indicador"] == "cov_aps"), None)
    assert row is not None
    assert row["pares"] == 2
    assert abs(row["mape"] - 15.0) < 1e-6

    # Drill-down
    r2 = client.get("/rdqa/consistencia/cov_aps/detalhes", params={"periodo": "2025-01"})
    assert r2.status_code == 200
    details = r2.json()
    assert any(d["chave"] == "mun=1" and abs(d["erro_pct"] - 10.0) < 1e-6 for d in details)
    assert any(d["chave"] == "mun=2" and abs(d["erro_pct"] - 20.0) < 1e-6 for d in details)

