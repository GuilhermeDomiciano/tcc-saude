from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.core.db import get_session
from app.services.unidade_service import UnidadeService
from app.schemas.unidade import DimUnidadeOut


router = APIRouter(prefix="/dw/unidades")


@router.get("", response_model=list[DimUnidadeOut])
def list_unidades(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    uf: Optional[str] = Query(None, min_length=2, max_length=2),
    session: Session = Depends(get_session),
):
    service = UnidadeService()
    return service.list(session, limit=limit, offset=offset, uf=uf)

