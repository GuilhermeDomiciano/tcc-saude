import os
from functools import lru_cache
from dataclasses import dataclass


@dataclass
class Settings:
    app_name: str = "Saúde API"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    allowed_origins: list[str] = tuple(
        o.strip() for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

