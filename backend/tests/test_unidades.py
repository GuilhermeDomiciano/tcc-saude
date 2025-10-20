def test_unidades_list_and_create(client):
    # initial list (from seed) should be >= 2
    r = client.get("/dw/unidades")
    assert r.status_code == 200
    base_len = len(r.json())

    # create
    payload = {
        "cnes": "9999999",
        "nome": "UBS Teste",
        "tipo_estabelecimento": "UBS",
        "bairro": "Centro",
        "territorio_id": 1,
        "gestao": "Municipal",
    }
    r = client.post("/dw/unidades", json=payload)
    assert r.status_code == 201, r.text

    # list again
    r2 = client.get("/dw/unidades")
    assert r2.status_code == 200
    assert len(r2.json()) >= base_len + 1

