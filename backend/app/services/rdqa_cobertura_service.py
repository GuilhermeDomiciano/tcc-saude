from __future__ import annotations

from typing import Dict, List, Optional

from sqlmodel import Session, select

from app.models.dev_lite import DevRefIndicador, DevCalcIndicador
from app.models.stage import RefIndicador, CalcIndicador


class RDQACoberturaService:
    def _models(self, session: Session):
        dialect = session.get_bind().dialect.name if session.get_bind() else ''
        if dialect == 'sqlite':
            return DevRefIndicador, DevCalcIndicador
        return RefIndicador, CalcIndicador

    def cobertura(self, session: Session, periodo: Optional[str] = None) -> Dict:
        Ref, Calc = self._models(session)
        try:
            stmt_ref = select(Ref)
            stmt_calc = select(Calc)
            if periodo:
                stmt_ref = stmt_ref.where(Ref.periodo == periodo)
                stmt_calc = stmt_calc.where(Calc.periodo == periodo)
            ref_rows = session.exec(stmt_ref).all()
            calc_rows = session.exec(stmt_calc).all()
        except Exception:
            ref_rows, calc_rows = [], []

        ref_keys = {(r.indicador, r.chave, r.periodo) for r in ref_rows}
        calc_keys = {(c.indicador, c.chave, c.periodo) for c in calc_rows}

        total = len(ref_keys)
        gerados = len(ref_keys & calc_keys)
        faltantes_items: List[Dict[str, str]] = []
        for (indicador, chave, per) in sorted(ref_keys - calc_keys):
            faltantes_items.append({
                "quadro": f"{indicador}:{chave}",
                "periodo": per,
                "motivo": "sem dados",
            })
        percent = (gerados / total * 100.0) if total else 0.0
        return {
            "percent": percent,
            "total": total,
            "gerados": gerados,
            "faltantes": faltantes_items,
        }
