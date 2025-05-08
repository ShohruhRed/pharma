"""add stage_id to predictions

Revision ID: af6924a3f181
Revises: 6b90ccd418a0
Create Date: 2025-05-08 11:49:39.498388

"""
from alembic import op
import sqlalchemy as sa

# идентификаторы ревизии
revision = 'af6924a3f181'
down_revision = '6b90ccd418a0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1) Добавляем колонку stage_id
    op.add_column(
        'predictions',
        sa.Column('stage_id', sa.Integer(), nullable=True)
    )
    # 2) Создаём внешний ключ к таблице stages
    op.create_foreign_key(
        'fk_predictions_stage_id_stages',
        source_table='predictions',
        referent_table='stages',
        local_cols=['stage_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    # 1) Удаляем внешний ключ
    op.drop_constraint(
        'fk_predictions_stage_id_stages',
        'predictions',
        type_='foreignkey'
    )
    # 2) Удаляем колонку stage_id
    op.drop_column('predictions', 'stage_id')
