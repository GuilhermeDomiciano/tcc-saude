from typing import Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel
from sqlmodel import Session

from app.core.db import get_session
from app.services.rdqa_export_service import RDQAExportService


router = APIRouter(prefix="/rdqa")


class ExportPDFIn(BaseModel):
    html: Optional[str] = None
    url: Optional[str] = None
    format: str = 'A4'
    margin_mm: int = 12


exporter = RDQAExportService()


@router.post(
    "/export/pdf",
    responses={
        200: {
            "content": {"application/pdf": {}},
            "description": "PDF gerado a partir de HTML ou URL",
            "headers": {
                "X-Exec-Id": {"description": "Identificador da execução", "schema": {"type": "string"}},
                "X-Hash": {"description": "SHA-256 do conteúdo PDF", "schema": {"type": "string"}},
                "Content-Disposition": {"description": "Sugestão de nome do arquivo", "schema": {"type": "string"}},
            },
        }
    },
)
async def export_pdf(payload: ExportPDFIn, session: Session = Depends(get_session)):
    try:
        if not payload.html and not payload.url:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="informe 'html' ou 'url'")
        if payload.html:
            pdf_bytes = await exporter.render_pdf_from_html(payload.html, format_=payload.format, margin_mm=payload.margin_mm)
        else:
            pdf_bytes = await exporter.render_pdf_from_url(payload.url or '', format_=payload.format, margin_mm=payload.margin_mm)
        exec_id = str(uuid.uuid4())
        pdf_hash = exporter.sha256_hex(pdf_bytes)
        headers = {
            'X-Exec-Id': exec_id,
            'X-Hash': pdf_hash,
            'Content-Disposition': 'inline; filename="rdqa.pdf"',
        }
        return Response(content=pdf_bytes, media_type='application/pdf', headers=headers)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"erro ao gerar PDF: {e}")
