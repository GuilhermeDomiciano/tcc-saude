from fastapi.testclient import TestClient


def test_rag_resumo(client: TestClient):
    resp = client.get("/rag/resumo")
    assert resp.status_code == 200
    data = resp.json()
    assert "itens" in data
    assert isinstance(data["itens"], list)
    assert len(data["itens"]) >= 1
    first = data["itens"][0]
    assert "territorio_id" in first
    assert "execucao_percentual" in first


def test_rag_financeiro_por_territorio(client: TestClient):
    resp = client.get("/rag/financeiro", params={"territorio_id": 1})
    assert resp.status_code == 200
    rows = resp.json()
    assert rows
    assert all(row["territorio_id"] == 1 for row in rows)


def test_rag_producao(client: TestClient):
    resp = client.get("/rag/producao", params={"periodo": "2024"})
    assert resp.status_code == 200
    rows = resp.json()
    assert rows
    assert all(row["periodo"] == "2024" for row in rows)


def test_rag_metas_cumprida_flag(client: TestClient):
    resp = client.get("/rag/metas", params={"periodo": "2024"})
    assert resp.status_code == 200
    rows = resp.json()
    assert rows
    assert "cumprida" in rows[0]


def test_rag_export_pdf_requer_html_ou_url(client: TestClient):
    resp = client.post("/rag/export/pdf", json={})
    assert resp.status_code == 400
    data = resp.json()
    assert data["detail"] == "informe 'html' ou 'url'"
