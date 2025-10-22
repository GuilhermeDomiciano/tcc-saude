import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[2]
for entry in [str(BACKEND_DIR), str(ROOT)]:
    if entry not in sys.path:
        sys.path.insert(0, entry)

from sqlmodel import Session, select

from app.core.db import engine
from app.models.dev_lite import DevRefIndicador, DevCalcIndicador, DevArtefatoExecucao
from app.models.stage import RawIngest
from app.workers.ingest_rdqa import ingest_rdqa_payload


def test_ingest_rdqa_payload_atualiza_tabelas(client):
    payload = {
        "referencia": [
            {"indicador": "cov_aps", "chave": "mun=1", "periodo": "2024-12", "valor": 90.0}
        ],
        "calculado": [
            {"indicador": "cov_aps", "chave": "mun=1", "periodo": "2024-12", "valor": 87.0}
        ],
    }
    with Session(engine) as session:
        exec_id = ingest_rdqa_payload(session, payload=payload, fonte="planilha_teste", periodo_ref="2024-12")

        ref_row = session.exec(
            select(DevRefIndicador).where(
                DevRefIndicador.indicador == "cov_aps",
                DevRefIndicador.chave == "mun=1",
                DevRefIndicador.periodo == "2024-12",
            )
        ).first()
        assert ref_row is not None
        assert ref_row.valor == 90.0

        calc_row = session.exec(
            select(DevCalcIndicador).where(
                DevCalcIndicador.indicador == "cov_aps",
                DevCalcIndicador.chave == "mun=1",
                DevCalcIndicador.periodo == "2024-12",
            )
        ).first()
        assert calc_row is not None
        assert calc_row.valor == 87.0

        bind = session.get_bind()
        dialect = bind.dialect.name if bind else ""
        if dialect != "sqlite":
            raw = session.get(RawIngest, exec_id)
            assert raw is not None
        artefato = session.get(DevArtefatoExecucao, str(exec_id))
        assert artefato is not None
        assert artefato.tipo == "rdqa_ingest"




