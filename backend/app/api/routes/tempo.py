from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.core.db import get_session
from app.services.tempo_service import TempoService
from app.schemas.tempo import DimTempoOut


router = APIRouter(prefix="/dw/tempo")


@router.get("", response_model=list[DimTempoOut])
def list_tempo(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    ano: Optional[int] = Query(None, ge=1900, le=2100),
    mes: Optional[int] = Query(None, ge=1, le=12),
    session: Session = Depends(get_session),
):
    service = TempoService()
    return service.list(session, limit=limit, offset=offset, ano=ano, mes=mes)

