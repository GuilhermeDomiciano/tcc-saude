from fastapi import APIRouter, Depends, Query

from sqlmodel import Session

from app.core.db import get_session
from app.services.territorio_service import TerritorioService
from app.schemas.territorio import DimTerritorioOut


router = APIRouter(prefix="/dw/territorios")


@router.get("", response_model=list[DimTerritorioOut])
def list_territorios(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    service = TerritorioService()
    return service.list(session, limit=limit, offset=offset)

