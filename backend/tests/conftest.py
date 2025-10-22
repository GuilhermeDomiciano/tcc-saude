import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./dev_test.db"
os.environ.pop("API_KEY", None)

# Ensure backend package is importable when running from repo root
ROOT = Path(__file__).resolve().parents[1].parents[0]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="session")
def client() -> TestClient:
    # Use SQLite dev DB and no API key by default (writes open for tests)
    from backend.app.core.db import engine
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)

    from backend.main import app

    with TestClient(app) as c:
        yield c






