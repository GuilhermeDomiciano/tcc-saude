from fastapi import APIRouter
from .routes.health import router as health_router
from .routes.territorios import router as territorios_router
from .routes.unidades import router as unidades_router
from .routes.tempo import router as tempo_router
from .routes.fatos import router as fatos_router


api_router = APIRouter()
api_router.include_router(health_router, tags=["health"]) 
api_router.include_router(territorios_router, tags=["dw"]) 
api_router.include_router(unidades_router, tags=["dw"]) 
api_router.include_router(tempo_router, tags=["dw"]) 
api_router.include_router(fatos_router, tags=["dw"]) 
