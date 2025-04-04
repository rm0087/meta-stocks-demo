"""goodwill

Revision ID: 14627aabb4cd
Revises: 36c6c7551034
Create Date: 2024-10-03 01:47:43.865152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14627aabb4cd'
down_revision = '36c6c7551034'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bs_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('goodwill', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bs_table', schema=None) as batch_op:
        batch_op.drop_column('goodwill')

    # ### end Alembic commands ###
