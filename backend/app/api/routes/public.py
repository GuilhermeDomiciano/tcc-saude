from typing import Optional
from fastapi import APIRouter, Query


router = APIRouter(prefix="/public")


@router.get("/verificar")
def verificar(exec_id: Optional[str] = Query(None), hash: Optional[str] = Query(None)):
    return {
        "ok": False,
        "exec_id": exec_id,
        "hash": hash,
        "status": "indisponivel",
        "message": "verificação ainda não implementada (stub)",
    }

