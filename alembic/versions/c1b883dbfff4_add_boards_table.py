"""add boards table

Revision ID: c1b883dbfff4
Revises: b764aaedf10d
Create Date: 2017-10-30 19:37:00.544958

"""
# pylint: skip-file

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c1b883dbfff4'
down_revision = 'b764aaedf10d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('boards',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('task_number', sa.Integer(), nullable=False),
                    sa.Column(
                        'created_at',
                        sa.DateTime(timezone=True),
                        server_default=sa.text('now()'),
                        nullable=False),
                    sa.Column(
                        'updated_at',
                        sa.DateTime(timezone=True),
                        server_default=sa.text('now()'),
                        nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_boards')))
    op.add_column('tasks', sa.Column('board_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        op.f('fk_tasks_board_id_boards'), 'tasks', 'boards', ['board_id'],
        ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f('fk_tasks_board_id_boards'), 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'board_id')
    op.drop_table('boards')
    # ### end Alembic commands ###
