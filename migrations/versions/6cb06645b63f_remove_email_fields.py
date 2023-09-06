"""remove email fields

Revision ID: 6cb06645b63f
Revises: bbe59dd44695
Create Date: 2023-08-13 14:33:32.964056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cb06645b63f'
down_revision = 'bbe59dd44695'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('username')
        batch_op.drop_column('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=120), nullable=False))
        batch_op.add_column(sa.Column('username', sa.VARCHAR(length=80), nullable=False))

    # ### end Alembic commands ###
