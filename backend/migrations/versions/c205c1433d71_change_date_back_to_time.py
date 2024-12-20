"""change date back to time

Revision ID: c205c1433d71
Revises: 1c8ce2d9ae75
Create Date: 2024-11-29 12:43:47.459491

"""
from alembic import op
import sqlalchemy as sa
import backend

# revision identifiers, used by Alembic.
revision = 'c205c1433d71'
down_revision = '1c8ce2d9ae75'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.drop_column('date')
        batch_op.add_column(sa.Column('date', sa.TIMESTAMP(timezone=False), nullable=True))


def downgrade():
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.drop_column('date')
        batch_op.add_column(sa.Column('date', sa.VARCHAR(length=255), nullable=True))
