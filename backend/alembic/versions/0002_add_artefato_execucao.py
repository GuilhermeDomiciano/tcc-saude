"""add artefato_execucao table for verification

Revision ID: 0002_add_artefato
Revises: 0001_init_dw_stage
Create Date: 2025-10-21 00:00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0002_add_artefato'
down_revision = '0001_init_dw_stage'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name

    op.create_table(
        'artefato_execucao',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('hash_sha256', sa.Text(), nullable=False),
        sa.Column('tipo', sa.Text(), nullable=False),
        sa.Column('fonte', sa.Text(), nullable=True),
        sa.Column('periodo', sa.Text(), nullable=True),
        sa.Column('versao', sa.Text(), nullable=True),
        sa.Column('autor', sa.Text(), nullable=True),
        sa.Column('metadados', sa.Text(), nullable=True),
        sa.Column('ok', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('mensagem', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()') if dialect != 'sqlite' else None, nullable=False),
        schema=None if dialect == 'sqlite' else 'dw'
    )


def downgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name
    op.drop_table('artefato_execucao', schema=None if dialect == 'sqlite' else 'dw')

