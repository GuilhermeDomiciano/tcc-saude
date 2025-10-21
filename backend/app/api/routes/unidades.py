from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session

from app.core.db import get_session
from app.services.unidade_service import UnidadeService
from app.schemas.unidade import DimUnidadeOut, DimUnidadeCreate, DimUnidadeUpdate
from app.core.security import require_api_key


router = APIRouter(prefix="/dw/unidades")


@router.get("", response_model=list[DimUnidadeOut])
def list_unidades(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    uf: Optional[str] = Query(None, min_length=2, max_length=2),
    cnes: Optional[str] = Query(None),
    territorio_id: Optional[int] = Query(None, ge=1),
    session: Session = Depends(get_session),
    ):
    service = UnidadeService()
    return service.list(session, limit=limit, offset=offset, uf=uf, cnes=cnes, territorio_id=territorio_id)


@router.post("", response_model=DimUnidadeOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_api_key)])
def create_unidade(payload: DimUnidadeCreate, session: Session = Depends(get_session)):
    service = UnidadeService()
    try:
        return service.create(session, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{id}", response_model=DimUnidadeOut, dependencies=[Depends(require_api_key)])
def update_unidade(id: int, payload: DimUnidadeUpdate, session: Session = Depends(get_session)):
    service = UnidadeService()
    try:
        updated = service.update(session, id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unidade não encontrada")
    return updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_api_key)])
def delete_unidade(id: int, session: Session = Depends(get_session)):
    service = UnidadeService()
    ok = service.delete(session, id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unidade não encontrada")
    return None


