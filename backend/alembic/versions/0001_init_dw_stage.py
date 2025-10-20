"""init dw and stage schemas and tables

Revision ID: 0001_init_dw_stage
Revises: 
Create Date: 2025-10-20 00:00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001_init_dw_stage'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect != 'sqlite':
        op.execute('CREATE SCHEMA IF NOT EXISTS dw')
        op.execute('CREATE SCHEMA IF NOT EXISTS stage')

    # dw.dim_territorio
    op.create_table(
        'dim_territorio',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('cod_ibge_municipio', sa.String(length=7), nullable=False),
        sa.Column('nome', sa.Text(), nullable=False),
        sa.Column('uf', sa.String(length=2), nullable=False),
        sa.Column('area_km2', sa.Numeric(12, 3), nullable=True),
        sa.Column('pop_censo_2022', sa.Integer(), nullable=True),
        sa.Column('pop_estim_2024', sa.Integer(), nullable=True),
        sa.UniqueConstraint('cod_ibge_municipio', name='uq_dim_territorio_ibge'),
        schema=None if dialect == 'sqlite' else 'dw'
    )

    # dw.dim_unidade
    op.create_table(
        'dim_unidade',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('cnes', sa.String(length=7), nullable=False),
        sa.Column('nome', sa.Text(), nullable=False),
        sa.Column('tipo_estabelecimento', sa.Text(), nullable=True),
        sa.Column('bairro', sa.Text(), nullable=True),
        sa.Column('territorio_id', sa.BigInteger(), nullable=True),
        sa.Column('gestao', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['territorio_id'], ['dw.dim_territorio.id'] if dialect != 'sqlite' else ['dim_territorio.id']),
        sa.UniqueConstraint('cnes', name='uq_dim_unidade_cnes'),
        schema=None if dialect == 'sqlite' else 'dw'
    )

    # dw.dim_equipe
    op.create_table(
        'dim_equipe',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('id_equipe', sa.Text(), nullable=False),
        sa.Column('tipo', sa.Text(), nullable=False),
        sa.Column('unidade_id', sa.BigInteger(), nullable=True),
        sa.Column('territorio_id', sa.BigInteger(), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.ForeignKeyConstraint(['unidade_id'], ['dw.dim_unidade.id'] if dialect != 'sqlite' else ['dim_unidade.id']),
        sa.ForeignKeyConstraint(['territorio_id'], ['dw.dim_territorio.id'] if dialect != 'sqlite' else ['dim_territorio.id']),
        sa.UniqueConstraint('id_equipe', name='uq_dim_equipe_id_equipe'),
        schema=None if dialect == 'sqlite' else 'dw'
    )

    # dw.dim_fonte_recurso
    op.create_table(
        'dim_fonte_recurso',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('codigo', sa.Text(), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=False),
        sa.UniqueConstraint('codigo', name='uq_dim_fonte_codigo'),
        schema=None if dialect == 'sqlite' else 'dw'
    )

    # dw.dim_tempo
    op.create_table(
        'dim_tempo',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('data', sa.Date(), nullable=False),
        sa.Column('ano', sa.SmallInteger(), nullable=False),
        sa.Column('mes', sa.SmallInteger(), nullable=False),
        sa.Column('trimestre', sa.SmallInteger(), nullable=False),
        sa.Column('quadrimestre', sa.SmallInteger(), nullable=False),
        sa.Column('mes_nome', sa.Text(), nullable=True),
        sa.UniqueConstraint('data', name='uq_dim_tempo_data'),
        schema=None if dialect == 'sqlite' else 'dw'
    )

    # dw.dim_pop_faixa_etaria
    op.create_table(
        'dim_pop_faixa_etaria',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('territorio_id', sa.BigInteger(), nullable=False),
        sa.Column('ano', sa.SmallInteger(), nullable=False),
        sa.Column('faixa_etaria', sa.Text(), nullable=False),
        sa.Column('sexo', sa.String(length=1), nullable=False),
        sa.Column('populacao', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['territorio_id'], ['dw.dim_territorio.id'] if dialect != 'sqlite' else ['dim_territorio.id']),
        sa.UniqueConstraint('territorio_id', 'ano', 'faixa_etaria', 'sexo', name='uq_pop_faixa_comp'),
        schema=None if dialect == 'sqlite' else 'dw'
    )

    # dw.fato_cobertura_aps
    op.create_table(
        'fato_cobertura_aps',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('data', sa.Date(), nullable=False),
        sa.Column('tempo_id', sa.BigInteger(), nullable=False),
        sa.Column('territorio_id', sa.BigInteger(), nullable=False),
        sa.Column('equipe_id', sa.BigInteger(), nullable=True),
        sa.Column('tipo_equipe', sa.Text(), nullable=False),
        sa.Column('cobertura_percentual', sa.Numeric(), nullable=False),
        sa.Column('pop_coberta_estimada', sa.Integer(), nullable=True),
        sa.Column('extract_ts', sa.DateTime(timezone=True), server_default=sa.text('now()') if dialect != 'sqlite' else None, nullable=False),
        sa.ForeignKeyConstraint(['tempo_id'], ['dw.dim_tempo.id'] if dialect != 'sqlite' else ['dim_tempo.id']),
        sa.ForeignKeyConstraint(['territorio_id'], ['dw.dim_territorio.id'] if dialect != 'sqlite' else ['dim_territorio.id']),
        sa.ForeignKeyConstraint(['equipe_id'], ['dw.dim_equipe.id'] if dialect != 'sqlite' else ['dim_equipe.id']),
        schema=None if dialect == 'sqlite' else 'dw'
    )

    # dw.fato_eventos_vitais
    op.create_table(
        'fato_eventos_vitais',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('data', sa.Date(), nullable=False),
        sa.Column('tempo_id', sa.BigInteger(), nullable=False),
        sa.Column('territorio_id', sa.BigInteger(), nullable=False),
        sa.Column('nascidos_vivos', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('obitos_gerais', sa.Integer(), nullable=True),
        sa.Column('fonte', sa.Text(), nullable=True),
        sa.Column('extract_ts', sa.DateTime(timezone=True), server_default=sa.text('now()') if dialect != 'sqlite' else None, nullable=False),
        sa.ForeignKeyConstraint(['tempo_id'], ['dw.dim_tempo.id'] if dialect != 'sqlite' else ['dim_tempo.id']),
        sa.ForeignKeyConstraint(['territorio_id'], ['dw.dim_territorio.id'] if dialect != 'sqlite' else ['dim_territorio.id']),
        schema=None if dialect == 'sqlite' else 'dw'
    )

    # dw.fato_financas
    op.create_table(
        'fato_financas',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('data', sa.Date(), nullable=False),
        sa.Column('tempo_id', sa.BigInteger(), nullable=False),
        sa.Column('territorio_id', sa.BigInteger(), nullable=False),
        sa.Column('fonte_id', sa.BigInteger(), nullable=True),
        sa.Column('dotacao_atualizada_anual', sa.Numeric(), nullable=True),
        sa.Column('receita_realizada', sa.Numeric(), nullable=True),
        sa.Column('empenhado', sa.Numeric(), nullable=True),
        sa.Column('liquidado', sa.Numeric(), nullable=True),
        sa.Column('pago', sa.Numeric(), nullable=True),
        sa.Column('extract_ts', sa.DateTime(timezone=True), server_default=sa.text('now()') if dialect != 'sqlite' else None, nullable=False),
        sa.ForeignKeyConstraint(['tempo_id'], ['dw.dim_tempo.id'] if dialect != 'sqlite' else ['dim_tempo.id']),
        sa.ForeignKeyConstraint(['territorio_id'], ['dw.dim_territorio.id'] if dialect != 'sqlite' else ['dim_territorio.id']),
        sa.ForeignKeyConstraint(['fonte_id'], ['dw.dim_fonte_recurso.id'] if dialect != 'sqlite' else ['dim_fonte_recurso.id']),
        schema=None if dialect == 'sqlite' else 'dw'
    )

    # dw.fato_rede_fisica
    op.create_table(
        'fato_rede_fisica',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('data', sa.Date(), nullable=False),
        sa.Column('tempo_id', sa.BigInteger(), nullable=False),
        sa.Column('territorio_id', sa.BigInteger(), nullable=False),
        sa.Column('tipo_unidade', sa.Text(), nullable=False),
        sa.Column('quantidade', sa.Integer(), nullable=False),
        sa.Column('extract_ts', sa.DateTime(timezone=True), server_default=sa.text('now()') if dialect != 'sqlite' else None, nullable=False),
        sa.ForeignKeyConstraint(['tempo_id'], ['dw.dim_tempo.id'] if dialect != 'sqlite' else ['dim_tempo.id']),
        sa.ForeignKeyConstraint(['territorio_id'], ['dw.dim_territorio.id'] if dialect != 'sqlite' else ['dim_territorio.id']),
        schema=None if dialect == 'sqlite' else 'dw'
    )

    # stage.raw_ingest
    op.create_table(
        'raw_ingest',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('fonte', sa.Text(), nullable=False),
        sa.Column('periodo_ref', sa.Text(), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=False),
        sa.Column('ingested_at', sa.DateTime(timezone=True), nullable=False),
        schema=None if dialect == 'sqlite' else 'stage'
    )


def downgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name

    # Drop in reverse dependency order
    op.drop_table('raw_ingest', schema=None if dialect == 'sqlite' else 'stage')
    op.drop_table('fato_rede_fisica', schema=None if dialect == 'sqlite' else 'dw')
    op.drop_table('fato_financas', schema=None if dialect == 'sqlite' else 'dw')
    op.drop_table('fato_eventos_vitais', schema=None if dialect == 'sqlite' else 'dw')
    op.drop_table('fato_cobertura_aps', schema=None if dialect == 'sqlite' else 'dw')
    op.drop_table('dim_pop_faixa_etaria', schema=None if dialect == 'sqlite' else 'dw')
    op.drop_table('dim_fonte_recurso', schema=None if dialect == 'sqlite' else 'dw')
    op.drop_table('dim_equipe', schema=None if dialect == 'sqlite' else 'dw')
    op.drop_table('dim_unidade', schema=None if dialect == 'sqlite' else 'dw')
    op.drop_table('dim_tempo', schema=None if dialect == 'sqlite' else 'dw')
    op.drop_table('dim_territorio', schema=None if dialect == 'sqlite' else 'dw')

    if dialect != 'sqlite':
        op.execute('DROP SCHEMA IF EXISTS stage CASCADE')
        op.execute('DROP SCHEMA IF EXISTS dw CASCADE')

