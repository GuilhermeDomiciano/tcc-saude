import io
import json
import zipfile

from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_export_pacote_returns_zip_and_manifest():
    r = client.post("/rdqa/export/pacote")
    assert r.status_code == 200
    assert r.headers.get("content-type").startswith("application/zip")
    exec_id = r.headers.get("x-exec-id")
    zip_hash = r.headers.get("x-hash")
    assert exec_id
    assert zip_hash

    buf = io.BytesIO(r.content)
    with zipfile.ZipFile(buf) as z:
        names = z.namelist()
        assert "MANIFEST.json" in names
        assert any(n.startswith("data/dim_territorio") for n in names)
        mf = json.loads(z.read("MANIFEST.json").decode("utf-8"))
        assert mf.get("exec_id") == exec_id

