from fastapi.testclient import TestClient
from backend.main import app
from app.core.db import engine
from sqlmodel import Session, select
from app.models.dev_lite import DevCalcIndicador


client = TestClient(app)


def seed_diff(indicador: str = "cov_aps", per_prev: str = "2025-01", per_curr: str = "2025-02"):
    with Session(engine) as session:
        rows = session.exec(select(DevCalcIndicador).where(DevCalcIndicador.indicador == indicador, DevCalcIndicador.periodo.in_([per_prev, per_curr]))).all()
        for r in rows:
            session.delete(r)
        session.commit()

        session.add_all([
            DevCalcIndicador(indicador=indicador, chave="mun=1", periodo=per_prev, valor=50.0),
            DevCalcIndicador(indicador=indicador, chave="mun=2", periodo=per_prev, valor=70.0),
        ])
        session.add_all([
            DevCalcIndicador(indicador=indicador, chave="mun=1", periodo=per_curr, valor=55.0),
            DevCalcIndicador(indicador=indicador, chave="mun=2", periodo=per_curr, valor=65.0),
            DevCalcIndicador(indicador=indicador, chave="mun=3", periodo=per_curr, valor=10.0),
        ])
        session.commit()


def test_rdqa_diff_endpoint():
    seed_diff()
    r = client.get("/rdqa/diff", params={"periodo_atual": "2025-02", "periodo_anterior": "2025-01", "indicadores": "cov_aps"})
    assert r.status_code == 200
    rows = r.json()
    d1 = next(x for x in rows if x["chave"] == "mun=1")
    d2 = next(x for x in rows if x["chave"] == "mun=2")
    assert d1["tendencia"] == "melhora"
    assert d2["tendencia"] == "piora"
    d3 = next(x for x in rows if x["chave"] == "mun=3")
    assert d3["delta"] is None

