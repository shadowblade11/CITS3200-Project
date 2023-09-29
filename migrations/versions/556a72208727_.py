"""empty message

Revision ID: 556a72208727
Revises: 798dedc3ba63
Create Date: 2023-09-29 13:28:22.280992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '556a72208727'
down_revision = '798dedc3ba63'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('complete',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('test_id', sa.Integer(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['test_id'], ['test.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('complete')
    # ### end Alembic commands ###
