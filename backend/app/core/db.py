import os
from typing import Iterator

from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv, find_dotenv


def _load_envs() -> None:
    # Load root .env then backend/.env if present; later files don't override existing values
    root_env = find_dotenv(filename=".env", raise_error_if_not_found=False)
    if root_env:
        load_dotenv(dotenv_path=root_env, override=False)
    backend_env = find_dotenv(filename="backend/.env", raise_error_if_not_found=False)
    if backend_env:
        load_dotenv(dotenv_path=backend_env, override=False)


def _build_engine_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///./dev.db")


def get_engine():
    url = _build_engine_url()
    if url.startswith("sqlite"):
        return create_engine(url, connect_args={"check_same_thread": False})
    return create_engine(url, pool_pre_ping=True)


_load_envs()
engine = get_engine()


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
