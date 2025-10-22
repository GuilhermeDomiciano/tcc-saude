from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from sqlmodel import Session, select

from app.models.dev_lite import (
    DevDimTerritorio,
    DevFatoRAGFinanceiro,
    DevFatoRAGProducao,
    DevFatoRAGMeta,
)
from app.models import dw as dw_models


class RAGService:
    def _models(self, session: Session) -> Dict[str, object]:
        dialect = session.get_bind().dialect.name if session.get_bind() else ""
        if dialect == "sqlite":
            return {
                "territorio": DevDimTerritorio,
                "financeiro": DevFatoRAGFinanceiro,
                "producao": DevFatoRAGProducao,
                "meta": DevFatoRAGMeta,
            }
        return {
            "territorio": dw_models.DimTerritorio,
            "financeiro": dw_models.FatoRAGFinanceiro,
            "producao": dw_models.FatoRAGProducao,
            "meta": dw_models.FatoRAGMeta,
        }

    def _territorios(self, session: Session, territorio_model, territorio_id: Optional[int]) -> Dict[int, str]:
        stmt = select(territorio_model)
        if territorio_id is not None:
            stmt = stmt.where(territorio_model.id == territorio_id)
        rows = session.exec(stmt).all()
        return {r.id: getattr(r, "nome", None) for r in rows}

    def financeiro(self, session: Session, *, periodo: Optional[str] = None, territorio_id: Optional[int] = None):
        models = self._models(session)
        Model = models["financeiro"]
        stmt = select(Model)
        if periodo:
            stmt = stmt.where(Model.periodo == periodo)
        if territorio_id is not None:
            stmt = stmt.where(Model.territorio_id == territorio_id)
        rows = session.exec(stmt).all()
        territorios = self._territorios(session, models["territorio"], territorio_id)
        out: List[Dict[str, object]] = []
        for row in rows:
            out.append({
                "territorio_id": row.territorio_id,
                "territorio_nome": territorios.get(row.territorio_id),
                "periodo": row.periodo,
                "dotacao_atualizada": getattr(row, "dotacao_atualizada", None),
                "receita_realizada": getattr(row, "receita_realizada", None),
                "empenhado": getattr(row, "empenhado", None),
                "liquidado": getattr(row, "liquidado", None),
                "pago": getattr(row, "pago", None),
            })
        return out

    def producao(self, session: Session, *, periodo: Optional[str] = None, territorio_id: Optional[int] = None):
        models = self._models(session)
        Model = models["producao"]
        stmt = select(Model)
        if periodo:
            stmt = stmt.where(Model.periodo == periodo)
        if territorio_id is not None:
            stmt = stmt.where(Model.territorio_id == territorio_id)
        rows = session.exec(stmt).all()
        territorios = self._territorios(session, models["territorio"], territorio_id)
        out: List[Dict[str, object]] = []
        for row in rows:
            out.append({
                "territorio_id": row.territorio_id,
                "territorio_nome": territorios.get(row.territorio_id),
                "periodo": row.periodo,
                "tipo": getattr(row, "tipo", ""),
                "quantidade": getattr(row, "quantidade", None),
            })
        return out

    def metas(self, session: Session, *, periodo: Optional[str] = None, territorio_id: Optional[int] = None):
        models = self._models(session)
        Model = models["meta"]
        stmt = select(Model)
        if periodo:
            stmt = stmt.where(Model.periodo == periodo)
        if territorio_id is not None:
            stmt = stmt.where(Model.territorio_id == territorio_id)
        rows = session.exec(stmt).all()
        territorios = self._territorios(session, models["territorio"], territorio_id)
        out: List[Dict[str, object]] = []
        for row in rows:
            planejada = getattr(row, "meta_planejada", None)
            executada = getattr(row, "meta_executada", None)
            cumprida = None
            try:
                if planejada is not None and executada is not None and planejada != 0:
                    cumprida = executada >= planejada
            except Exception:
                cumprida = None
            out.append({
                "territorio_id": row.territorio_id,
                "territorio_nome": territorios.get(row.territorio_id),
                "periodo": row.periodo,
                "indicador": getattr(row, "indicador", ""),
                "meta_planejada": planejada,
                "meta_executada": executada,
                "cumprida": cumprida,
            })
        return out

    def resumo(self, session: Session, *, periodo: Optional[str] = None, territorio_id: Optional[int] = None):
        financeiros = self.financeiro(session, periodo=periodo, territorio_id=territorio_id)
        producoes = self.producao(session, periodo=periodo, territorio_id=territorio_id)
        metas = self.metas(session, periodo=periodo, territorio_id=territorio_id)

        resumo: Dict[Tuple[int, str], Dict[str, object]] = {}
        periodos = set()

        for row in financeiros:
            key = (row["territorio_id"], row["periodo"])
            periodos.add(row["periodo"])
            data = resumo.setdefault(key, {
                "territorio_id": row["territorio_id"],
                "territorio_nome": row.get("territorio_nome"),
                "periodo": row["periodo"],
                "dotacao_atualizada": 0.0,
                "receita_realizada": 0.0,
                "empenhado": 0.0,
                "liquidado": 0.0,
                "pago": 0.0,
                "producao_total": 0,
                "metas_cumpridas": 0,
                "metas_total": 0,
            })
            for field in ["dotacao_atualizada", "receita_realizada", "empenhado", "liquidado", "pago"]:
                value = row.get(field)
                if value is not None:
                    data[field] = float(value)

        for row in producoes:
            key = (row["territorio_id"], row["periodo"])
            periodos.add(row["periodo"])
            data = resumo.setdefault(key, {
                "territorio_id": row["territorio_id"],
                "territorio_nome": row.get("territorio_nome"),
                "periodo": row["periodo"],
                "dotacao_atualizada": 0.0,
                "receita_realizada": 0.0,
                "empenhado": 0.0,
                "liquidado": 0.0,
                "pago": 0.0,
                "producao_total": 0,
                "metas_cumpridas": 0,
                "metas_total": 0,
            })
            qtd = row.get("quantidade")
            if qtd is not None:
                data["producao_total"] = (data.get("producao_total") or 0) + int(qtd)

        for row in metas:
            key = (row["territorio_id"], row["periodo"])
            periodos.add(row["periodo"])
            data = resumo.setdefault(key, {
                "territorio_id": row["territorio_id"],
                "territorio_nome": row.get("territorio_nome"),
                "periodo": row["periodo"],
                "dotacao_atualizada": 0.0,
                "receita_realizada": 0.0,
                "empenhado": 0.0,
                "liquidado": 0.0,
                "pago": 0.0,
                "producao_total": 0,
                "metas_cumpridas": 0,
                "metas_total": 0,
            })
            data["metas_total"] = int(data.get("metas_total", 0) + 1)
            if row.get("cumprida") is True:
                data["metas_cumpridas"] = int(data.get("metas_cumpridas", 0) + 1)

        itens: List[Dict[str, object]] = []
        for key, data in resumo.items():
            dotacao = data.get("dotacao_atualizada")
            pago = data.get("pago")
            execucao = None
            try:
                if dotacao and dotacao > 0 and pago is not None:
                    execucao = (float(pago) / float(dotacao)) * 100.0
            except Exception:
                execucao = None
            data["execucao_percentual"] = execucao
            itens.append(data)

        itens.sort(key=lambda d: (d["periodo"], d["territorio_id"]))
        return {
            "periodos": sorted(periodos),
            "itens": itens,
        }
