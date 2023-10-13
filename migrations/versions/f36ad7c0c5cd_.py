"""empty message

Revision ID: f36ad7c0c5cd
Revises: bd1625f147ab
Create Date: 2023-10-03 23:48:08.110752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f36ad7c0c5cd'
down_revision = 'bd1625f147ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('complete', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
        batch_op.drop_column('completed_id')

    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
        batch_op.drop_column('feedback_id')

    with op.batch_alter_table('score', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
        batch_op.drop_column('score_id')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('score', schema=None) as batch_op:
        batch_op.add_column(sa.Column('score_id', sa.INTEGER(), nullable=False))
        batch_op.drop_column('id')

    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.add_column(sa.Column('feedback_id', sa.INTEGER(), nullable=False))
        batch_op.drop_column('id')

    with op.batch_alter_table('complete', schema=None) as batch_op:
        batch_op.add_column(sa.Column('completed_id', sa.INTEGER(), nullable=False))
        batch_op.drop_column('id')

    # ### end Alembic commands ###
