from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ValueError)
    async def handle_value_error(_: Request, exc: ValueError):
        return JSONResponse(status_code=400, content={"detail": str(exc) or "Invalid value"})

    @app.exception_handler(IntegrityError)
    async def handle_integrity_error(_: Request, exc: IntegrityError):
        return JSONResponse(status_code=409, content={"detail": "Conflict: integrity constraint violation"})

