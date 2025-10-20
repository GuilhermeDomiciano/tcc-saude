from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.core.db import get_session
from app.services.fatos_service import FatosService
from app.schemas.fatos import FatoCoberturaAPSOut


router = APIRouter(prefix="/dw/fatos")


@router.get("/cobertura", response_model=list[FatoCoberturaAPSOut])
def list_cobertura(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    data_ini: Optional[date] = Query(None),
    data_fim: Optional[date] = Query(None),
    territorio_id: Optional[int] = Query(None, ge=1),
    session: Session = Depends(get_session),
):
    service = FatosService()
    return service.list_cobertura(
        session,
        limit=limit,
        offset=offset,
        data_ini=data_ini,
        data_fim=data_fim,
        territorio_id=territorio_id,
    )

