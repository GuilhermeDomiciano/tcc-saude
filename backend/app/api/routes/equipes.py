from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session

from app.core.db import get_session
from app.services.equipe_service import EquipeService
from app.schemas.equipe import DimEquipeOut, DimEquipeCreate, DimEquipeUpdate
from app.core.security import require_api_key


router = APIRouter(prefix="/dw/equipes")


@router.get("", response_model=list[DimEquipeOut])
def list_equipes(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    service = EquipeService()
    return service.list(session, limit=limit, offset=offset)


@router.post("", response_model=DimEquipeOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_api_key)])
def create_equipe(payload: DimEquipeCreate, session: Session = Depends(get_session)):
    service = EquipeService()
    try:
        return service.create(session, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{id}", response_model=DimEquipeOut, dependencies=[Depends(require_api_key)])
def update_equipe(id: int, payload: DimEquipeUpdate, session: Session = Depends(get_session)):
    service = EquipeService()
    try:
        updated = service.update(session, id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipe não encontrada")
    return updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_api_key)])
def delete_equipe(id: int, session: Session = Depends(get_session)):
    service = EquipeService()
    ok = service.delete(session, id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipe não encontrada")
    return None
