from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from sqlmodel import Session, delete

from app.core.db import engine
from app.models.stage import RawIngest, RefIndicador as StageRefIndicador, CalcIndicador as StageCalcIndicador
from app.models.dev_lite import DevRefIndicador, DevCalcIndicador
from app.services.artefato_service import ArtefatoService
from app.services.rdqa_export_service import RDQAExportService


def _hash_payload(payload: Dict[str, Any]) -> str:
    data = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return RDQAExportService.sha256_hex(data)  # reuse util


def _resolve_models(session: Session):
    dialect = session.get_bind().dialect.name if session.get_bind() else ""
    if dialect == "sqlite":
        return DevRefIndicador, DevCalcIndicador
    return StageRefIndicador, StageCalcIndicador


def ingest_rdqa_payload(
    session: Session,
    *,
    payload: Dict[str, Any],
    fonte: str,
    periodo_ref: str,
    registrar_artefato: bool = True,
) -> uuid.UUID:
    """Ingestão de dados RDQA a partir de dicionário estruturado."""
    ref_items = list(payload.get("referencia", []))
    calc_items = list(payload.get("calculado", []))

    dialect = session.get_bind().dialect.name if session.get_bind() else ""
    use_stage_raw = dialect != "sqlite"
    raw_id: uuid.UUID

    if use_stage_raw:
        raw = RawIngest(fonte=fonte, periodo_ref=periodo_ref, payload=payload)
        session.add(raw)
        session.commit()
        session.refresh(raw)
        raw_id = raw.id
    else:
        raw_id = uuid.uuid4()

    RefModel, CalcModel = _resolve_models(session)

    for item in ref_items:
        indicador = item.get("indicador")
        chave = item.get("chave")
        periodo = item.get("periodo", periodo_ref)
        valor = item.get("valor")
        if indicador is None or chave is None or valor is None:
            continue
        session.exec(
            delete(RefModel).where(
                RefModel.indicador == indicador,
                RefModel.chave == chave,
                RefModel.periodo == periodo,
            )
        )
        session.add(RefModel(indicador=indicador, chave=chave, periodo=periodo, valor=float(valor)))

    for item in calc_items:
        indicador = item.get("indicador")
        chave = item.get("chave")
        periodo = item.get("periodo", periodo_ref)
        valor = item.get("valor")
        if indicador is None or chave is None or valor is None:
            continue
        session.exec(
            delete(CalcModel).where(
                CalcModel.indicador == indicador,
                CalcModel.chave == chave,
                CalcModel.periodo == periodo,
            )
        )
        session.add(CalcModel(indicador=indicador, chave=chave, periodo=periodo, valor=float(valor)))

    session.commit()

    if registrar_artefato:
        artefatos = ArtefatoService()
        artefatos.registrar_execucao(
            session,
            exec_id=str(raw_id),
            hash_sha256=_hash_payload(payload),
            tipo="rdqa_ingest",
            fonte=fonte,
            periodo=periodo_ref,
            metadados=json.dumps({"referencia": len(ref_items), "calculado": len(calc_items)}),
        )
    return raw_id


def ingest_rdqa_file(path: Path, *, fonte: str, periodo_ref: str, registrar_artefato: bool = True) -> uuid.UUID:
    payload = json.loads(path.read_text(encoding="utf-8"))
    with Session(engine) as session:
        return ingest_rdqa_payload(
            session,
            payload=payload,
            fonte=fonte,
            periodo_ref=periodo_ref,
            registrar_artefato=registrar_artefato,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingestão de planilha RDQA (JSON) para stage/dev.")
    parser.add_argument("arquivo", type=Path, help="Caminho do arquivo JSON estruturado.")
    parser.add_argument("--fonte", required=True, help="Identificador da fonte (ex.: 'planilha_oficial_q4').")
    parser.add_argument("--periodo", required=True, help="Período de referência (ex.: 2024-12).")
    args = parser.parse_args()

    exec_id = ingest_rdqa_file(args.arquivo, fonte=args.fonte, periodo_ref=args.periodo)
    print(f"[ingest] planejamento concluído. exec_id={exec_id}")


if __name__ == "__main__":  # pragma: no cover
    main()
