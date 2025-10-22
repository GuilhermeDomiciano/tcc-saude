from typing import List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlmodel import Session

from app.core.db import get_session
from app.core.security import require_api_key
from app.schemas.rag import (
    RAGExportIn,
    RAGFinanceiroOut,
    RAGMetaOut,
    RAGProducaoOut,
    RAGResumoOut,
)
from app.services.rag_service import RAGService
from app.services.rdqa_export_service import RDQAExportService
from app.services.artefato_service import ArtefatoService


router = APIRouter(prefix="/rag", tags=["rag"])

service = RAGService()
exporter = RDQAExportService()
artefatos = ArtefatoService()


@router.get("/resumo", response_model=RAGResumoOut, summary="Painel consolidado do RAG por território")
def obter_resumo(
    periodo: Optional[str] = Query(None, description="Período (ex.: 2024)"),
    territorio_id: Optional[int] = Query(None, description="Filtrar por ID do território"),
    session: Session = Depends(get_session),
):
    data = service.resumo(session, periodo=periodo, territorio_id=territorio_id)
    return data


@router.get("/financeiro", response_model=List[RAGFinanceiroOut], summary="Detalhes financeiros do RAG")
def listar_financeiro(
    periodo: Optional[str] = Query(None, description="Período (ex.: 2024)"),
    territorio_id: Optional[int] = Query(None, description="Filtrar por ID do território"),
    session: Session = Depends(get_session),
):
    return service.financeiro(session, periodo=periodo, territorio_id=territorio_id)


@router.get("/producao", response_model=List[RAGProducaoOut], summary="Dados de produção assistencial do RAG")
def listar_producao(
    periodo: Optional[str] = Query(None, description="Período (ex.: 2024)"),
    territorio_id: Optional[int] = Query(None, description="Filtrar por ID do território"),
    session: Session = Depends(get_session),
):
    return service.producao(session, periodo=periodo, territorio_id=territorio_id)


@router.get("/metas", response_model=List[RAGMetaOut], summary="Indicadores de metas do RAG")
def listar_metas(
    periodo: Optional[str] = Query(None, description="Período (ex.: 2024)"),
    territorio_id: Optional[int] = Query(None, description="Filtrar por ID do território"),
    session: Session = Depends(get_session),
):
    return service.metas(session, periodo=periodo, territorio_id=territorio_id)


@router.post(
    "/export/pdf",
    responses={
        200: {
            "content": {"application/pdf": {}},
            "description": "PDF do quadro RAG (Financeiro/Metas/etc.)",
            "headers": {
                "X-Exec-Id": {"description": "Identificador da execução", "schema": {"type": "string"}},
                "X-Hash": {"description": "SHA-256 do conteúdo PDF", "schema": {"type": "string"}},
                "Content-Disposition": {"description": "Sugestão de nome do arquivo", "schema": {"type": "string"}},
            },
        }
    },
)
async def exportar_pdf(
    payload: RAGExportIn,
    session: Session = Depends(get_session),
    _: None = Depends(require_api_key),
):
    if not payload.html and not payload.url:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="informe 'html' ou 'url'")
    try:
        if payload.html:
            pdf_bytes = await exporter.render_pdf_from_html(payload.html, format_=payload.format, margin_mm=payload.margin_mm)
        else:
            pdf_bytes = await exporter.render_pdf_from_url(payload.url or "", format_=payload.format, margin_mm=payload.margin_mm)
        exec_id = str(uuid.uuid4())
        pdf_hash = exporter.sha256_hex(pdf_bytes)
        try:
            artefatos.registrar_execucao(
                session,
                exec_id=exec_id,
                hash_sha256=pdf_hash,
                tipo="rag_pdf",
            )
        except Exception:
            pass
        headers = {
            "X-Exec-Id": exec_id,
            "X-Hash": pdf_hash,
            "Content-Disposition": 'inline; filename="rag.pdf"',
        }
        return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"erro ao gerar PDF: {exc}")
