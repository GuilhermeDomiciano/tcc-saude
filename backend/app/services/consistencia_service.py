from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from sqlmodel import Session, select

from app.models.dev_lite import DevRefIndicador, DevCalcIndicador
from app.models.stage import RefIndicador, CalcIndicador


@dataclass
class IndicadorMAPE:
    indicador: str
    periodo: Optional[str]
    mape: Optional[float]
    pares: int


class ConsistenciaService:
    def _models(self, session: Session):
        dialect = session.get_bind().dialect.name if session.get_bind() else ''
        if dialect == 'sqlite':
            return DevRefIndicador, DevCalcIndicador
        return RefIndicador, CalcIndicador

    def calcular_mape(self, session: Session, indicador: str, periodo: Optional[str] = None) -> IndicadorMAPE:
        Ref, Calc = self._models(session)
        stmt_ref = select(Ref).where(Ref.indicador == indicador)
        stmt_calc = select(Calc).where(Calc.indicador == indicador)
        if periodo:
            stmt_ref = stmt_ref.where(Ref.periodo == periodo)
            stmt_calc = stmt_calc.where(Calc.periodo == periodo)
        ref_rows = session.exec(stmt_ref).all()
        calc_rows = session.exec(stmt_calc).all()
        ref_map: Dict[Tuple[str, str], float] = {(r.chave, r.periodo): float(r.valor) for r in ref_rows}
        calc_map: Dict[Tuple[str, str], float] = {(c.chave, c.periodo): float(c.valor) for c in calc_rows}
        errors: List[float] = []
        for key, ref_val in ref_map.items():
            if key in calc_map:
                if ref_val == 0:
                    continue  # ignora para evitar div/0
                err = abs((calc_map[key] - ref_val) / ref_val) * 100.0
                errors.append(err)
        mape = sum(errors) / len(errors) if errors else None
        return IndicadorMAPE(indicador=indicador, periodo=periodo, mape=mape, pares=len(errors))

    def listar_indicadores(self, session: Session, periodo: Optional[str] = None) -> List[IndicadorMAPE]:
        Ref, Calc = self._models(session)
        stmt_ref = select(Ref.indicador).distinct()
        if periodo:
            stmt_ref = stmt_ref.where(Ref.periodo == periodo)
        indicadores = [row[0] if isinstance(row, tuple) else row for row in session.exec(stmt_ref).all()]
        out: List[IndicadorMAPE] = []
        for ind in indicadores:
            out.append(self.calcular_mape(session, ind, periodo))
        return out

    def drill_down(self, session: Session, indicador: str, periodo: Optional[str] = None) -> List[Dict[str, float | str]]:
        Ref, Calc = self._models(session)
        stmt_ref = select(Ref).where(Ref.indicador == indicador)
        stmt_calc = select(Calc).where(Calc.indicador == indicador)
        if periodo:
            stmt_ref = stmt_ref.where(Ref.periodo == periodo)
            stmt_calc = stmt_calc.where(Calc.periodo == periodo)
        ref_rows = session.exec(stmt_ref).all()
        calc_rows = session.exec(stmt_calc).all()
        calc_map: Dict[Tuple[str, str], float] = {(c.chave, c.periodo): float(c.valor) for c in calc_rows}
        out: List[Dict[str, float | str]] = []
        for r in ref_rows:
            key = (r.chave, r.periodo)
            cval = calc_map.get(key)
            row = {
                "indicador": r.indicador,
                "chave": r.chave,
                "periodo": r.periodo,
                "ref": float(r.valor),
                "calc": float(cval) if cval is not None else None,
            }
            if cval is not None and r.valor != 0:
                erro_abs = abs(float(cval) - float(r.valor))
                erro_pct = abs((float(cval) - float(r.valor)) / float(r.valor)) * 100.0
                row["erro_abs"] = erro_abs
                row["erro_pct"] = erro_pct
            out.append(row)
        # ordenar por maior erro_pct primeiro (quando existir)
        out.sort(key=lambda d: d.get("erro_pct", -1.0), reverse=True)
        return out

