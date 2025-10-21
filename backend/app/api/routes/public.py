from typing import Optional
from fastapi import APIRouter, Query, Depends
from sqlmodel import Session

from app.core.db import get_session
from app.services.artefato_service import ArtefatoService


router = APIRouter(prefix="/public")
svc = ArtefatoService()


@router.get("/verificar")
def verificar(exec_id: Optional[str] = Query(None), hash: Optional[str] = Query(None), session: Session = Depends(get_session)):
    return svc.verificar(session, exec_id=exec_id, hash_value=hash)
