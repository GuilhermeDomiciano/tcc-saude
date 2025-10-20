from typing import Optional

from fastapi import Header, HTTPException, status

from app.core.config import get_settings


def require_api_key(x_api_key: Optional[str] = Header(None)) -> None:
    settings = get_settings()
    if not settings.api_key:
        return
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")

