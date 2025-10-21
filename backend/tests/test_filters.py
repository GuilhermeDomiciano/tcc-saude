from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_territorios_filter_uf():
    r = client.get("/dw/territorios", params={"uf": "RS", "limit": 100})
    assert r.status_code == 200
    items = r.json()
    assert all(it["uf"] == "RS" for it in items)


def test_territorios_filter_ibge_prefix():
    r = client.get("/dw/territorios", params={"cod_ibge_municipio": "43", "limit": 100})
    assert r.status_code == 200
    items = r.json()
    assert all(it["cod_ibge_municipio"].startswith("43") for it in items)


def test_unidades_filters_cnes_and_territorio():
    r1 = client.get("/dw/unidades", params={"cnes": "0000001"})
    assert r1.status_code == 200
    items1 = r1.json()
    assert all(it["cnes"].startswith("0000001") for it in items1)

    r2 = client.get("/dw/unidades", params={"territorio_id": 1})
    assert r2.status_code == 200
    items2 = r2.json()
    assert all(it.get("territorio_id") == 1 for it in items2)


def test_equipes_filters_accept_params():
    # Without seed, ensure the endpoint accepts and returns 200
    r = client.get("/dw/equipes", params={"tipo": "ESF", "ativo": True})
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_fontes_filter_accept_param():
    r = client.get("/dw/fontes", params={"codigo": "001"})
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_public_verificar_stub():
    r = client.get("/public/verificar", params={"exec_id": "abc", "hash": "def"})
    assert r.status_code == 200
    body = r.json()
    assert body["exec_id"] == "abc"
    assert body["hash"] == "def"
    assert "status" in body

