from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session

from app.core.db import get_session
from app.services.fonte_service import FonteService
from app.schemas.fonte import DimFonteRecursoOut, DimFonteRecursoCreate, DimFonteRecursoUpdate


router = APIRouter(prefix="/dw/fontes")


@router.get("", response_model=list[DimFonteRecursoOut])
def list_fontes(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    service = FonteService()
    return service.list(session, limit=limit, offset=offset)


@router.post("", response_model=DimFonteRecursoOut, status_code=status.HTTP_201_CREATED)
def create_fonte(payload: DimFonteRecursoCreate, session: Session = Depends(get_session)):
    service = FonteService()
    try:
        return service.create(session, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{id}", response_model=DimFonteRecursoOut)
def update_fonte(id: int, payload: DimFonteRecursoUpdate, session: Session = Depends(get_session)):
    service = FonteService()
    try:
        updated = service.update(session, id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fonte não encontrada")
    return updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fonte(id: int, session: Session = Depends(get_session)):
    service = FonteService()
    ok = service.delete(session, id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fonte não encontrada")
    return None

