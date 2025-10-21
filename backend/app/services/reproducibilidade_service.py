from __future__ import annotations

import io
import json
import uuid
import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from zipfile import ZipFile, ZIP_DEFLATED

from sqlmodel import Session, select

from app.models import dw as dw_models
from app.models import dev_lite as dev_models


class ReproducibilidadeService:
    def _is_sqlite(self, session: Session) -> bool:
        return (session.get_bind().dialect.name if session.get_bind() else '') == 'sqlite'

    def _models(self, session: Session):
        if self._is_sqlite(session):
            return {
                "dim_territorio": dev_models.DevDimTerritorio,
                "dim_unidade": dev_models.DevDimUnidade,
                "dim_tempo": dev_models.DevDimTempo,
                "dim_pop_faixa_etaria": dev_models.DevDimPopFaixaEtaria,
                "dim_fonte_recurso": dev_models.DevDimFonteRecurso,
                "dim_equipe": dev_models.DevDimEquipe,
                "fato_cobertura_aps": dev_models.DevFatoCoberturaAPS,
            }
        else:
            return {
                "dim_territorio": dw_models.DimTerritorio,
                "dim_unidade": dw_models.DimUnidade,
                "dim_tempo": dw_models.DimTempo,
                "dim_pop_faixa_etaria": dw_models.DimPopFaixaEtaria,
                "dim_fonte_recurso": dw_models.DimFonteRecurso,
                "dim_equipe": dw_models.DimEquipe,
                "fato_cobertura_aps": dw_models.FatoCoberturaAPS,
            }

    @staticmethod
    def _sha256_hex(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def _jsonify(self, d: Dict[str, Any]) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        for k, v in d.items():
            if hasattr(v, 'isoformat'):
                out[k] = v.isoformat()
            elif hasattr(v, 'value') and isinstance(getattr(v, 'value'), (str, int, float, bool)):
                out[k] = v.value  # Enum
            else:
                try:
                    json.dumps(v)
                    out[k] = v
                except Exception:
                    out[k] = str(v)
        return out

    def _dump_query(self, session: Session, model, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        stmt = select(model)
        try:
            rows = session.exec(stmt).all()
        except Exception:
            return []
        out: List[Dict[str, Any]] = []
        for r in rows:
            if hasattr(r, 'model_dump'):
                d = r.model_dump()
            elif hasattr(r, 'dict'):
                d = r.dict()
            else:
                try:
                    fields = r.__fields__.keys()  # type: ignore[attr-defined]
                    d = {k: getattr(r, k) for k in fields}
                except Exception:
                    d = {k: v for k, v in vars(r).items() if not k.startswith('_')}
            d = self._jsonify(d)
            out.append(d)
        return out

    def gerar_pacote(self, session: Session, *, periodo: Optional[str] = None) -> Tuple[bytes, str, str]:
        models = self._models(session)
        buf = io.BytesIO()
        manifest: Dict[str, Any] = {
            "schema": 1,
            "generated_at": datetime.utcnow().isoformat() + 'Z',
            "exec_id": str(uuid.uuid4()),
            "periodo": periodo,
            "files": [],
        }
        with ZipFile(buf, 'w', compression=ZIP_DEFLATED) as z:
            # README
            readme = (
                "Pacote de Reprodutibilidade (RDQA)\n\n"
                "Conteúdos:\n"
                "- data/*.json: dumps das dimensões e fatos relevantes.\n"
                "- MANIFEST.json: metadados do pacote.\n\n"
                "Como usar:\n"
                "- Importe os JSONs em seu ambiente de análise ou gere seeds a partir deles.\n"
            )
            z.writestr('README.txt', readme)
            manifest["files"].append({"path": "README.txt", "size": len(readme)})

            # data dumps
            for name, model in models.items():
                data = self._dump_query(session, model)
                j = json.dumps(data, ensure_ascii=False, indent=2)
                path = f"data/{name}.json"
                z.writestr(path, j)
                manifest["files"].append({"path": path, "size": len(j)})

            z.writestr('MANIFEST.json', json.dumps(manifest, ensure_ascii=False, indent=2))

        zip_bytes = buf.getvalue()
        pkg_hash = self._sha256_hex(zip_bytes)
        return zip_bytes, manifest["exec_id"], pkg_hash
