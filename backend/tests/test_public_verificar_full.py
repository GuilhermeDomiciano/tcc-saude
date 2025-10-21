from fastapi.testclient import TestClient
from backend.main import app
from app.core.db import engine
from sqlmodel import Session
from app.models.dev_lite import DevArtefatoExecucao


client = TestClient(app)


def test_public_verificar_ok_flow():
    # Arrange: inserir um artefato no dev-lite
    exec_id = "test-exec-123"
    hash_value = "abcd1234"
    with Session(engine) as session:
        # idempotente para rodar localmente múltiplas vezes
        row = session.get(DevArtefatoExecucao, exec_id)
        if not row:
            row = DevArtefatoExecucao(id=exec_id, hash_sha256=hash_value, tipo="rdqa_pdf")
            session.add(row)
            session.commit()

    # Act
    r = client.get("/public/verificar", params={"exec_id": exec_id, "hash": hash_value})

    # Assert
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["status"] == "valido"
    assert body["exec_id"] == exec_id
    assert body["hash"] == hash_value


def test_public_verificar_not_found():
    r = client.get("/public/verificar", params={"exec_id": "nao-existe", "hash": "zzz"})
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is False
    assert body["status"] in {"nao_encontrado", "invalido"}

