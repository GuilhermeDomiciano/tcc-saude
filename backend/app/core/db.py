import os
from contextlib import contextmanager
from typing import Iterator

from sqlmodel import SQLModel, Session, create_engine


def _build_engine_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///./dev.db")


def get_engine():
    url = _build_engine_url()
    if url.startswith("sqlite"):
        return create_engine(url, connect_args={"check_same_thread": False})
    return create_engine(url, pool_pre_ping=True)


engine = get_engine()


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session

