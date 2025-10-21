from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Session
import uuid

from app.core.db import get_session


router = APIRouter(prefix="/rdqa")


@router.post("/export/pdf")
def export_pdf(payload: dict, session: Session = Depends(get_session)):
    exec_id = str(uuid.uuid4())
    fake_hash = uuid.uuid5(uuid.NAMESPACE_URL, exec_id).hex
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "message": "Exportador PDF ainda não implementado (stub)",
            "exec_id": exec_id,
            "hash": fake_hash,
        },
    )

