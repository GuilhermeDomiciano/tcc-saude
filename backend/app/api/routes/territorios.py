from fastapi import APIRouter, Depends, Query, HTTPException, status

from sqlmodel import Session

from app.core.db import get_session
from app.services.territorio_service import TerritorioService
from app.schemas.territorio import DimTerritorioOut, DimTerritorioCreate, DimTerritorioUpdate
from app.core.security import require_api_key


router = APIRouter(prefix="/dw/territorios")


@router.get("", response_model=list[DimTerritorioOut])
def list_territorios(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    service = TerritorioService()
    return service.list(session, limit=limit, offset=offset)


@router.post("", response_model=DimTerritorioOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_api_key)])
def create_territorio(payload: DimTerritorioCreate, session: Session = Depends(get_session)):
    service = TerritorioService()
    try:
        return service.create(session, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{id}", response_model=DimTerritorioOut, dependencies=[Depends(require_api_key)])
def update_territorio(id: int, payload: DimTerritorioUpdate, session: Session = Depends(get_session)):
    service = TerritorioService()
    try:
        updated = service.update(session, id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Território não encontrado")
    return updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_api_key)])
def delete_territorio(id: int, session: Session = Depends(get_session)):
    service = TerritorioService()
    ok = service.delete(session, id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Território não encontrado")
    return None
