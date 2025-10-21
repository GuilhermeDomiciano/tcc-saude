from typing import Optional, List
import uuid

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import Response
from pydantic import BaseModel
from sqlmodel import Session

from app.core.db import get_session
from app.core.security import require_api_key
from app.services.rdqa_export_service import RDQAExportService
from app.services.artefato_service import ArtefatoService
from app.services.consistencia_service import ConsistenciaService
from app.services.rdqa_cobertura_service import RDQACoberturaService
from app.services.rdqa_diff_service import RDQADiffService
from app.services.reproducibilidade_service import ReproducibilidadeService
from app.services.rdqa_cobertura_service import RDQACoberturaService


router = APIRouter(prefix="/rdqa")


class ExportPDFIn(BaseModel):
    html: Optional[str] = None
    url: Optional[str] = None
    format: str = 'A4'
    margin_mm: int = 12


exporter = RDQAExportService()
artefatos = ArtefatoService()
consistencia = ConsistenciaService()
rdqa_cobertura = RDQACoberturaService()
rdqa_diff = RDQADiffService()
repro_pkg = ReproducibilidadeService()


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
async def export_pdf(payload: ExportPDFIn, session: Session = Depends(get_session), _: None = Depends(require_api_key)):
    try:
        if not payload.html and not payload.url:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="informe 'html' ou 'url'")
        if payload.html:
            pdf_bytes = await exporter.render_pdf_from_html(payload.html, format_=payload.format, margin_mm=payload.margin_mm)
        else:
            pdf_bytes = await exporter.render_pdf_from_url(payload.url or '', format_=payload.format, margin_mm=payload.margin_mm)
        exec_id = str(uuid.uuid4())
        pdf_hash = exporter.sha256_hex(pdf_bytes)
        # registrar execução/artefato
        try:
            artefatos.registrar_execucao(
                session,
                exec_id=exec_id,
                hash_sha256=pdf_hash,
                tipo="rdqa_pdf",
            )
        except Exception:
            # Não falhar geração de PDF por erro de registro
            pass
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


from app.schemas.rdqa import (
    ConsistenciaResumoOut,
    ConsistenciaDetalheOut,
    CoberturaOut,
    DiffRowOut,
)


@router.get("/consistencia", response_model=List[ConsistenciaResumoOut], summary="Lista MAPE por indicador")
def listar_consistencia(periodo: Optional[str] = Query(None, description="Período (ex.: 2025-01)"), session: Session = Depends(get_session)):
    res = consistencia.listar_indicadores(session, periodo)
    return [
        {"indicador": r.indicador, "periodo": r.periodo, "mape": r.mape, "pares": r.pares}
        for r in res
    ]


@router.get("/consistencia/{indicador}/detalhes", response_model=List[ConsistenciaDetalheOut], summary="Drill-down de divergências")
def detalhes_consistencia(indicador: str, periodo: Optional[str] = Query(None, description="Período"), session: Session = Depends(get_session)):
    return consistencia.drill_down(session, indicador, periodo)


@router.get("/cobertura", response_model=CoberturaOut, summary="Cobertura de quadros RDQA gerados")
def obter_cobertura(periodo: Optional[str] = Query(None, description="Período"), session: Session = Depends(get_session)):
    return rdqa_cobertura.cobertura(session, periodo)


@router.get("/diff", response_model=List[DiffRowOut], summary="Comparação entre períodos (diff)")
def diff(
    periodo_atual: str = Query(..., description="Período atual"),
    periodo_anterior: str = Query(..., description="Período anterior"),
    indicadores: Optional[str] = Query(None, description="Lista separada por vírgula"),
    session: Session = Depends(get_session),
):
    inds = [s.strip() for s in (indicadores.split(",") if indicadores else []) if s.strip()]
    if not inds:
        Model = rdqa_diff._model(session)
        rows = session.exec(select(Model.indicador).where(Model.periodo == periodo_atual).distinct()).all()
        inds = [row[0] if isinstance(row, tuple) else row for row in rows]
    return rdqa_diff.comparar(session, indicadores=inds, periodo_atual=periodo_atual, periodo_anterior=periodo_anterior)


@router.post(
    "/export/pacote",
    responses={
        200: {
            "content": {"application/zip": {}},
            "description": "Pacote de reprodutibilidade (ZIP)",
            "headers": {
                "X-Exec-Id": {"description": "Identificador da execução", "schema": {"type": "string"}},
                "X-Hash": {"description": "SHA-256 do conteúdo ZIP", "schema": {"type": "string"}},
                "Content-Disposition": {"description": "Sugestão de nome do arquivo", "schema": {"type": "string"}},
            },
        }
    },
)
def export_pacote(periodo: Optional[str] = None, session: Session = Depends(get_session), _: None = Depends(require_api_key)):
    try:
        zip_bytes, exec_id, pkg_hash = repro_pkg.gerar_pacote(session, periodo=periodo)
        # registrar artefato
        try:
            artefatos.registrar_execucao(session, exec_id=exec_id, hash_sha256=pkg_hash, tipo="rdqa_package")
        except Exception:
            pass
        headers = {
            'X-Exec-Id': exec_id,
            'X-Hash': pkg_hash,
            'Content-Disposition': 'attachment; filename="rdqa-package.zip"',
        }
        return Response(content=zip_bytes, media_type='application/zip', headers=headers)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"erro ao gerar pacote: {e}")
