from __future__ import annotations

from typing import Optional, Dict, Any

from sqlmodel import Session, select

from app.models.dw import ArtefatoExecucao as DWArtefatoExecucao
from app.models.dev_lite import DevArtefatoExecucao


class ArtefatoService:
    def _model(self, session: Session):
        dialect = session.get_bind().dialect.name if session.get_bind() else ''
        return DevArtefatoExecucao if dialect == 'sqlite' else DWArtefatoExecucao

    def registrar_execucao(
        self,
        session: Session,
        *,
        exec_id: str,
        hash_sha256: str,
        tipo: str = "rdqa_pdf",
        fonte: Optional[str] = None,
        periodo: Optional[str] = None,
        versao: Optional[str] = None,
        autor: Optional[str] = None,
        metadados: Optional[str] = None,
        ok: bool = True,
        mensagem: Optional[str] = None,
    ):
        Model = self._model(session)
        existing = session.get(Model, exec_id)
        if existing:
            existing.hash_sha256 = hash_sha256
            existing.tipo = tipo
            existing.fonte = fonte
            existing.periodo = periodo
            existing.versao = versao
            existing.autor = autor
            existing.metadados = metadados
            existing.ok = ok
            existing.mensagem = mensagem
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing
        row = Model(
            id=exec_id,
            hash_sha256=hash_sha256,
            tipo=tipo,
            fonte=fonte,
            periodo=periodo,
            versao=versao,
            autor=autor,
            metadados=metadados,
            ok=ok,
            mensagem=mensagem,
        )
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    def verificar(self, session: Session, *, exec_id: Optional[str], hash_value: Optional[str]) -> Dict[str, Any]:
        Model = self._model(session)
        if not exec_id or not hash_value:
            return {
                "ok": False,
                "exec_id": exec_id,
                "hash": hash_value,
                "status": "invalido",
                "message": "informe exec_id e hash",
            }
        row = session.get(Model, exec_id)
        if not row:
            return {
                "ok": False,
                "exec_id": exec_id,
                "hash": hash_value,
                "status": "nao_encontrado",
                "message": "execucao nao localizada",
            }
        ok = (row.hash_sha256 == hash_value)
        return {
            "ok": ok,
            "exec_id": exec_id,
            "hash": hash_value,
            "status": "valido" if ok else "hash_divergente",
            "tipo": getattr(row, 'tipo', None),
            "fonte": getattr(row, 'fonte', None),
            "periodo": getattr(row, 'periodo', None),
            "versao": getattr(row, 'versao', None),
            "autor": getattr(row, 'autor', None),
            "mensagem": getattr(row, 'mensagem', None),
            "created_at": getattr(row, 'created_at', None).isoformat() if getattr(row, 'created_at', None) else None,
        }

