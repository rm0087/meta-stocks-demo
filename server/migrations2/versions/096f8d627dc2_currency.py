"""currency

Revision ID: 096f8d627dc2
Revises: 7df2501b0269
Create Date: 2024-10-05 01:07:57.478534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '096f8d627dc2'
down_revision = '7df2501b0269'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inc_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('currency', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inc_table', schema=None) as batch_op:
        batch_op.drop_column('currency')

    # ### end Alembic commands ###
