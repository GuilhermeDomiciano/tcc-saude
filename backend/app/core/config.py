import os
from functools import lru_cache
from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv


@dataclass
class Settings:
    app_name: str = "Saúde API"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    allowed_origins: tuple[str, ...] = tuple(
        o.strip() for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    # Load root and backend .env for flexibility
    root_env = find_dotenv(filename=".env", raise_error_if_not_found=False)
    if root_env:
        load_dotenv(dotenv_path=root_env, override=False)
    backend_env = find_dotenv(filename="backend/.env", raise_error_if_not_found=False)
    if backend_env:
        load_dotenv(dotenv_path=backend_env, override=False)
    return Settings()
