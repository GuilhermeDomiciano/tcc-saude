def test_tempo_create_and_list(client):
    # Create a new month
    payload = {
        "data": "2025-03-01",
        "ano": 2025,
        "mes": 3,
        "trimestre": 1,
        "quadrimestre": 1,
        "mes_nome": "Março",
    }
    r = client.post("/dw/tempo", json=payload)
    assert r.status_code == 201, r.text
    created = r.json()
    assert created["mes"] == 3

    # List filtered by ano/mes
    r = client.get("/dw/tempo", params={"ano": 2025, "mes": 3})
    assert r.status_code == 200
    items = r.json()
    assert any(x["mes"] == 3 and x["ano"] == 2025 for x in items)

