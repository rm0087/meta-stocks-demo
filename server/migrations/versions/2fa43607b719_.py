"""empty message

Revision ID: 2fa43607b719
Revises: d2ae4c83eced
Create Date: 2024-09-29 22:14:59.965365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fa43607b719'
down_revision = 'd2ae4c83eced'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inc_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('revenue_key', sa.String(), nullable=True))
        batch_op.drop_column('key')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inc_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('key', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('revenue_key')

    # ### end Alembic commands ###
