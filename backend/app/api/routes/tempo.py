from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session

from app.core.db import get_session
from app.services.tempo_service import TempoService
from app.schemas.tempo import DimTempoOut, DimTempoCreate, DimTempoUpdate


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


@router.post("", response_model=DimTempoOut, status_code=status.HTTP_201_CREATED)
def create_tempo(payload: DimTempoCreate, session: Session = Depends(get_session)):
    service = TempoService()
    try:
        return service.create(session, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{id}", response_model=DimTempoOut)
def update_tempo(id: int, payload: DimTempoUpdate, session: Session = Depends(get_session)):
    service = TempoService()
    try:
        updated = service.update(session, id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tempo não encontrado")
    return updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tempo(id: int, session: Session = Depends(get_session)):
    service = TempoService()
    ok = service.delete(session, id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tempo não encontrado")
    return None
