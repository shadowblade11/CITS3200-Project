"""empty message

Revision ID: 1ea6b88185f8
Revises: bd1625f147ab
Create Date: 2023-09-29 12:58:44.214653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ea6b88185f8'
down_revision = 'bd1625f147ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('question')
    op.drop_table('score')
    op.drop_table('test')
    op.drop_table('complete')
    op.drop_table('feedback')
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

    op.create_table('feedback',
    sa.Column('feedback_id', sa.INTEGER(), nullable=False),
    sa.Column('feedback', sa.VARCHAR(length=512), nullable=True),
    sa.Column('test_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.VARCHAR(), nullable=False),
    sa.ForeignKeyConstraint(['test_id'], ['test.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('feedback_id')
    )
    op.create_table('complete',
    sa.Column('completed_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.VARCHAR(), nullable=False),
    sa.Column('test_id', sa.INTEGER(), nullable=False),
    sa.Column('completed', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['test_id'], ['test.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('completed_id')
    )
    op.create_table('test',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('week_number', sa.INTEGER(), nullable=True),
    sa.Column('test_name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('due_date', sa.VARCHAR(length=128), nullable=True),
    sa.Column('number_of_questions', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('score',
    sa.Column('score_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.VARCHAR(), nullable=False),
    sa.Column('question_id', sa.INTEGER(), nullable=False),
    sa.Column('user_score', sa.INTEGER(), nullable=True),
    sa.Column('sys_score', sa.INTEGER(), nullable=True),
    sa.Column('attempt_chosen', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('score_id')
    )
    op.create_table('question',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('question_name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('difficulty', sa.INTEGER(), nullable=True),
    sa.Column('test_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['test_id'], ['test.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###