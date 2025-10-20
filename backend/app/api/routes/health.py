from datetime import datetime
from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "ok",
        "time": datetime.utcnow().isoformat(),
    }

