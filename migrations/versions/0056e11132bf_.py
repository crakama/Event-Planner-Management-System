"""empty message

Revision ID: 0056e11132bf
Revises: 61dbcaa98262
Create Date: 2017-10-19 16:03:25.429662

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0056e11132bf'
down_revision = '61dbcaa98262'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'events_ibfk_1', 'events', type_='foreignkey')
    op.drop_column('events', 'task_id')
    op.add_column('tasks', sa.Column('event_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tasks', 'events', ['event_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'event_id')
    op.add_column('events', sa.Column('task_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key(u'events_ibfk_1', 'events', 'tasks', ['task_id'], ['id'])
    # ### end Alembic commands ###
