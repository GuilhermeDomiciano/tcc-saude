"""add stage tables for indicadores (ref and calc)

Revision ID: 0003_add_stage_indicadores
Revises: 0002_add_artefato
Create Date: 2025-10-21 00:05:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0003_add_stage_indicadores'
down_revision = '0002_add_artefato'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name

    op.create_table(
        'ref_indicador',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('indicador', sa.Text(), nullable=False),
        sa.Column('chave', sa.Text(), nullable=False),
        sa.Column('periodo', sa.Text(), nullable=False),
        sa.Column('valor', sa.Numeric(), nullable=False),
        schema=None if dialect == 'sqlite' else 'stage'
    )
    op.create_index('ix_stage_ref_indicador_keys', 'ref_indicador', ['indicador', 'periodo', 'chave'], unique=False, schema=None if dialect == 'sqlite' else 'stage')

    op.create_table(
        'calc_indicador',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('indicador', sa.Text(), nullable=False),
        sa.Column('chave', sa.Text(), nullable=False),
        sa.Column('periodo', sa.Text(), nullable=False),
        sa.Column('valor', sa.Numeric(), nullable=False),
        schema=None if dialect == 'sqlite' else 'stage'
    )
    op.create_index('ix_stage_calc_indicador_keys', 'calc_indicador', ['indicador', 'periodo', 'chave'], unique=False, schema=None if dialect == 'sqlite' else 'stage')


def downgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name
    op.drop_index('ix_stage_calc_indicador_keys', table_name='calc_indicador', schema=None if dialect == 'sqlite' else 'stage')
    op.drop_table('calc_indicador', schema=None if dialect == 'sqlite' else 'stage')
    op.drop_index('ix_stage_ref_indicador_keys', table_name='ref_indicador', schema=None if dialect == 'sqlite' else 'stage')
    op.drop_table('ref_indicador', schema=None if dialect == 'sqlite' else 'stage')

