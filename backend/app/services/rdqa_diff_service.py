from __future__ import annotations

from typing import Dict, List

from sqlmodel import Session, select

from app.models.dev_lite import DevCalcIndicador
from app.models.stage import CalcIndicador


class RDQADiffService:
    def _model(self, session: Session):
        dialect = session.get_bind().dialect.name if session.get_bind() else ''
        return DevCalcIndicador if dialect == 'sqlite' else CalcIndicador

    def comparar(
        self,
        session: Session,
        *,
        indicadores: List[str],
        periodo_atual: str,
        periodo_anterior: str,
    ) -> List[Dict[str, object]]:
        Model = self._model(session)
        res: List[Dict[str, object]] = []
        for indicador in indicadores:
            stmt_curr = select(Model).where(Model.indicador == indicador, Model.periodo == periodo_atual)
            stmt_prev = select(Model).where(Model.indicador == indicador, Model.periodo == periodo_anterior)
            curr_rows = session.exec(stmt_curr).all()
            prev_rows = session.exec(stmt_prev).all()
            curr_map: Dict[str, float] = {r.chave: float(r.valor) for r in curr_rows}
            prev_map: Dict[str, float] = {r.chave: float(r.valor) for r in prev_rows}
            keys = set(curr_map.keys()) | set(prev_map.keys())
            for k in sorted(keys):
                v_curr = curr_map.get(k)
                v_prev = prev_map.get(k)
                delta = (v_curr - v_prev) if (v_curr is not None and v_prev is not None) else None
                if v_curr is not None and v_prev is not None:
                    if v_curr > v_prev:
                        tendencia = "melhora"
                    elif v_curr < v_prev:
                        tendencia = "piora"
                    else:
                        tendencia = "igual"
                else:
                    tendencia = "igual"
                res.append({
                    "indicador": indicador,
                    "chave": k,
                    "periodo_atual": periodo_atual,
                    "periodo_anterior": periodo_anterior,
                    "valor_atual": v_curr,
                    "valor_anterior": v_prev,
                    "delta": delta,
                    "tendencia": tendencia,
                })
        return res

