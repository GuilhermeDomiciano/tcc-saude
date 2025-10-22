import os
import random
from datetime import date
from typing import Iterable

from sqlmodel import Session, SQLModel, create_engine, select, delete


def get_database_url() -> str:
    return os.getenv("DATABASE_URL") or "sqlite:///./dev.db"


def month_name_pt(m: int) -> str:
    nomes = [
        "Janeiro","Fevereiro","Março","Abril","Maio","Junho",
        "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"
    ]
    return nomes[m-1]


def iter_months(start: date, end: date) -> Iterable[date]:
    y, m = start.year, start.month
    while (y < end.year) or (y == end.year and m <= end.month):
        yield date(y, m, 1)
        if m == 12:
            y += 1
            m = 1
        else:
            m += 1


def seed_dev_sqlite(engine):
    from app.models.dev_lite import (
        DevDimTerritorio,
        DevDimUnidade,
        DevDimTempo,
        DevDimPopFaixaEtaria,
        DevDimFonteRecurso,
        DevDimEquipe,
        DevFatoRAGFinanceiro,
        DevFatoRAGProducao,
        DevFatoRAGMeta,
        DevRefIndicador,
        DevCalcIndicador,
    )

    SQLModel.metadata.create_all(bind=engine, tables=[
        DevDimTerritorio.__table__,
        DevDimUnidade.__table__,
        DevDimTempo.__table__,
        DevDimPopFaixaEtaria.__table__,
        DevDimFonteRecurso.__table__,
        DevDimEquipe.__table__,
        DevFatoRAGFinanceiro.__table__,
        DevFatoRAGProducao.__table__,
        DevFatoRAGMeta.__table__,
        DevRefIndicador.__table__,
        DevCalcIndicador.__table__,
    ])

    random.seed(42)
    ufs = ["TO"]
    cod_counter = {"TO": 1700000}
    municipios = []

    with Session(engine) as session:
        # wipe
        for model in [
            DevFatoRAGMeta,
            DevFatoRAGProducao,
            DevFatoRAGFinanceiro,
            DevCalcIndicador,
            DevRefIndicador,
            DevDimEquipe,
            DevDimFonteRecurso,
            DevDimPopFaixaEtaria,
            DevDimUnidade,
            DevDimTempo,
            DevDimTerritorio,
        ]:
            session.exec(delete(model))
        session.commit()

        # Territórios TO (~40)
        for uf in ufs:
            for i in range(40):
                cod_counter[uf] += 1
                cod = f"{cod_counter[uf]}"
                nome = f"Município {uf}-{i+1:02d}"
                area = round(random.uniform(50, 1500), 2)
                pop22 = random.randint(8000, 250000)
                pop24 = int(pop22 * random.uniform(0.98, 1.06))
                municipios.append((cod, nome, uf, area, pop22, pop24))
        session.add_all([
            DevDimTerritorio(
                cod_ibge_municipio=cod,
                nome=nome,
                uf=uf,
                area_km2=area,
                pop_censo_2022=pop22,
                pop_estim_2024=pop24,
            ) for (cod, nome, uf, area, pop22, pop24) in municipios
        ])
        session.commit()

        # Tempo: 2020-01..2025-12
        tempos = [
            DevDimTempo(
                data=d, ano=d.year, mes=d.month,
                trimestre=(d.month-1)//3 + 1,
                quadrimestre=(d.month-1)//4 + 1,
                mes_nome=month_name_pt(d.month),
            ) for d in iter_months(date(2020,1,1), date(2025,12,1))
        ]
        session.add_all(tempos)
        session.commit()

        # Unidades: 3..6 por município
        terr_rows = list(session.exec(select(DevDimTerritorio)))
        unidades = []
        for t in terr_rows:
            for j in range(random.randint(3,6)):
                unidades.append(DevDimUnidade(
                    cnes=f"{random.randint(1000000, 9999999)}",
                    nome=f"Unidade {t.uf}-{t.id}-{j+1:02d}",
                    tipo_estabelecimento=random.choice(["UBS","USF","UPA","HOSPITAL","POLICLÍNICA"]),
                    bairro=random.choice(["Centro","Norte","Sul","Leste","Oeste","Industrial","Universitário"]),
                    territorio_id=t.id,
                    gestao=random.choice(["Municipal","Estadual"]) if random.random()<0.9 else "Privada",
                ))
        session.add_all(unidades)
        session.commit()

        # Indicadores RDQA (referência e calculado) para cenários de consistência/diff
        ref_rows = []
        calc_rows = []
        for t in terr_rows[:10]:
            ref_val = random.uniform(70, 95)
            calc_val = ref_val * random.uniform(0.9, 1.1)
            chave = f"mun={t.id}"
            ref_rows.append(DevRefIndicador(indicador="cov_aps", chave=chave, periodo="2024-12", valor=round(ref_val, 2)))
            calc_rows.append(DevCalcIndicador(indicador="cov_aps", chave=chave, periodo="2024-12", valor=round(calc_val, 2)))
        session.add_all(ref_rows)
        session.add_all(calc_rows)
        session.commit()

        # População por faixa etária e sexo 2020..2025
        faixas = ["0-4","5-9","10-14","15-19","20-29","30-39","40-49","50-59","60-69","70-79","80+"]
        pop_rows = []
        for t in terr_rows:
            base = next((m[5] for m in municipios if m[0]==t.cod_ibge_municipio), 20000)
            for ano in range(2020, 2026):
                dist = [0.06,0.06,0.065,0.065,0.17,0.16,0.14,0.12,0.08,0.035,0.025]
                total_ano = int(base * (0.95 + 0.02*(ano-2020)))
                for i, faixa in enumerate(faixas):
                    faixa_total = int(total_ano * dist[i])
                    m = int(faixa_total * random.uniform(0.48, 0.52))
                    f = faixa_total - m
                    pop_rows.append(DevDimPopFaixaEtaria(territorio_id=t.id, ano=ano, faixa_etaria=faixa, sexo="M", populacao=m))
                    pop_rows.append(DevDimPopFaixaEtaria(territorio_id=t.id, ano=ano, faixa_etaria=faixa, sexo="F", populacao=f))
        session.add_all(pop_rows)
        session.commit()

        # Fontes de recurso
        fontes = [
            ("001","Tesouro Municipal"),
            ("002","Transferências Estaduais"),
            ("003","Transferências Federais"),
            ("004","Emendas Parlamentares"),
            ("005","Convênios"),
            ("006","Outras Fontes"),
        ]
        session.add_all([DevDimFonteRecurso(codigo=c, descricao=d) for c,d in fontes])
        session.commit()

        # Equipes 2..6 por unidade
        unidades_rows = list(session.exec(select(DevDimUnidade)))
        eq_types = ["ESF","ESB","ACS","OUTROS"]
        eqs = []
        for u in unidades_rows:
            for k in range(random.randint(2,6)):
                eqs.append(DevDimEquipe(
                    id_equipe=f"{u.id:04d}-{k+1:02d}",
                    tipo=random.choice(eq_types),
                    unidade_id=u.id,
                    territorio_id=u.territorio_id,
                    ativo=random.random()>0.1,
                ))
        session.add_all(eqs)
        session.commit()

        # RAG Financeiro
        rag_fin_rows = []
        for t in terr_rows[:10]:
            base = random.randint(2_000_000, 8_000_000)
            rag_fin_rows.append(DevFatoRAGFinanceiro(
                periodo="2024",
                territorio_id=t.id,
                dotacao_atualizada=base,
                receita_realizada=round(base * random.uniform(0.75, 0.95), 2),
                empenhado=round(base * random.uniform(0.6, 0.9), 2),
                liquidado=round(base * random.uniform(0.55, 0.85), 2),
                pago=round(base * random.uniform(0.5, 0.8), 2),
            ))
        session.add_all(rag_fin_rows)
        session.commit()

        # RAG Produção
        tipos_producao = ["Consultas ESF", "Visitas domiciliares", "Procedimentos odontológicos", "Atendimentos NASF"]
        rag_prod_rows = []
        for t in terr_rows[:10]:
            for tipo in tipos_producao:
                rag_prod_rows.append(DevFatoRAGProducao(
                    periodo="2024",
                    territorio_id=t.id,
                    tipo=tipo,
                    quantidade=random.randint(1000, 25000),
                ))
        session.add_all(rag_prod_rows)
        session.commit()

        # RAG Metas
        rag_meta_rows = []
        for t in terr_rows[:10]:
            rag_meta_rows.extend([
                DevFatoRAGMeta(
                    periodo="2024",
                    territorio_id=t.id,
                    indicador="cobertura_aps",
                    meta_planejada=round(random.uniform(75, 90), 2),
                    meta_executada=round(random.uniform(60, 95), 2),
                ),
                DevFatoRAGMeta(
                    periodo="2024",
                    territorio_id=t.id,
                    indicador="tempo_espera_consulta",
                    meta_planejada=7.0,
                    meta_executada=round(random.uniform(5, 12), 2),
                ),
            ])
        session.add_all(rag_meta_rows)
        session.commit()

    print("[seed] SQLite-dev: dados gerados para TO — territórios, tempo, unidades, pop_faixa, fontes e equipes.")


def seed_dw_postgres(engine):
    from app.models.dw import (DimTerritorio, DimTempo, DimUnidade, DimEquipe, DimFonteRecurso)
    with Session(engine) as session:
        for model in [DimEquipe, DimUnidade, DimFonteRecurso, DimTempo, DimTerritorio]:
            session.exec(delete(model))
        session.commit()
        session.add_all([
            DimFonteRecurso(codigo="001", descricao="Tesouro Municipal"),
            DimFonteRecurso(codigo="002", descricao="Estado"),
            DimFonteRecurso(codigo="003", descricao="União"),
        ])
        session.commit()
        print("[seed] Postgres-DW: dimensões básicas populadas (amostra).")


def main():
    engine = create_engine(get_database_url())
    if engine.dialect.name == 'sqlite':
        seed_dev_sqlite(engine)
    else:
        seed_dw_postgres(engine)


if __name__ == "__main__":
    main()
