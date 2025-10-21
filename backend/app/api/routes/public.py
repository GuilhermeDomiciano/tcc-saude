from typing import Optional
from fastapi import APIRouter, Query, Depends
from sqlmodel import Session

from app.core.db import get_session
from app.services.artefato_service import ArtefatoService
from app.schemas.rdqa import VerificacaoOut


router = APIRouter(prefix="/public")
svc = ArtefatoService()


@router.get("/verificar", response_model=VerificacaoOut, summary="Verifica integridade por exec_id/hash")
def verificar(exec_id: Optional[str] = Query(None, description="Identificador de execução"), hash: Optional[str] = Query(None, description="SHA-256 do artefato"), session: Session = Depends(get_session)):
    return svc.verificar(session, exec_id=exec_id, hash_value=hash)

