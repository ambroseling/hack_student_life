"""added ts vector

Revision ID: 8aba3faad011
Revises: c205c1433d71
Create Date: 2024-11-29 13:26:43.434656

"""
from alembic import op
import sqlalchemy as sa
import backend

# revision identifiers, used by Alembic.
revision = '8aba3faad011'
down_revision = 'c205c1433d71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ts_vector', backend.models.TSVector(), sa.Computed("to_tsvector('english', title || ' ' || description)", persisted=True), nullable=True))
        batch_op.create_index('ix_events_ts_vector', ['ts_vector'], unique=False, postgresql_using='gin')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.drop_index('ix_events_ts_vector', postgresql_using='gin')
        batch_op.drop_column('ts_vector')

    # ### end Alembic commands ###
