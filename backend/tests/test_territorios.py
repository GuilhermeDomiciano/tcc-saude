def test_crud_territorio(client):
    # Create
    payload = {
        "cod_ibge_municipio": "4300100",
        "nome": "Cidade Teste",
        "uf": "RS",
        "area_km2": 10.5,
    }
    r = client.post("/dw/territorios", json=payload)
    assert r.status_code == 201, r.text
    created = r.json()
    tid = created["id"]
    assert created["cod_ibge_municipio"] == payload["cod_ibge_municipio"]

    # List must include
    r = client.get("/dw/territorios")
    assert r.status_code == 200
    items = r.json()
    assert any(x["id"] == tid for x in items)

    # Update
    r = client.put(f"/dw/territorios/{tid}", json={"nome": "Cidade Atualizada"})
    assert r.status_code == 200
    assert r.json()["nome"] == "Cidade Atualizada"

    # Delete
    r = client.delete(f"/dw/territorios/{tid}")
    assert r.status_code == 204

