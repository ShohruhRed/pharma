"""Add SANFISPrediction table

Revision ID: fc1fdf8a0078
Revises: 1e0c643084f5
Create Date: 2025-04-13 16:38:15.683791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc1fdf8a0078'
down_revision: Union[str, None] = '1e0c643084f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sanfis_predictions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=False),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.Column('pressure', sa.Float(), nullable=True),
    sa.Column('humidity', sa.Float(), nullable=True),
    sa.Column('NaCl', sa.Float(), nullable=True),
    sa.Column('KCl', sa.Float(), nullable=True),
    sa.Column('defect_probability', sa.Float(), nullable=True),
    sa.Column('risk_level', sa.String(), nullable=True),
    sa.Column('recommendation', sa.String(), nullable=True),
    sa.Column('rule_used', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sanfis_predictions_id'), 'sanfis_predictions', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_sanfis_predictions_id'), table_name='sanfis_predictions')
    op.drop_table('sanfis_predictions')
    # ### end Alembic commands ###
