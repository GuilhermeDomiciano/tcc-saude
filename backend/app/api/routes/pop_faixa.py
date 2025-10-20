from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session

from app.core.db import get_session
from app.services.pop_faixa_service import PopFaixaService
from app.schemas.pop_faixa import (
    DimPopFaixaEtariaOut,
    DimPopFaixaEtariaCreate,
    DimPopFaixaEtariaUpdate,
)


router = APIRouter(prefix="/dw/pop-faixa")


@router.get("", response_model=list[DimPopFaixaEtariaOut])
def list_pop_faixa(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    territorio_id: Optional[int] = Query(None, ge=1),
    ano: Optional[int] = Query(None, ge=1900, le=2100),
    session: Session = Depends(get_session),
):
    service = PopFaixaService()
    return service.list(session, limit=limit, offset=offset, territorio_id=territorio_id, ano=ano)


@router.post("", response_model=DimPopFaixaEtariaOut, status_code=status.HTTP_201_CREATED)
def create_pop_faixa(payload: DimPopFaixaEtariaCreate, session: Session = Depends(get_session)):
    service = PopFaixaService()
    try:
        return service.create(session, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{id}", response_model=DimPopFaixaEtariaOut)
def update_pop_faixa(id: int, payload: DimPopFaixaEtariaUpdate, session: Session = Depends(get_session)):
    service = PopFaixaService()
    try:
        updated = service.update(session, id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro não encontrado")
    return updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pop_faixa(id: int, session: Session = Depends(get_session)):
    service = PopFaixaService()
    ok = service.delete(session, id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro não encontrado")
    return None

