"""empty message

Revision ID: db687ad98f56
Revises: b590f62c7e1c
Create Date: 2017-10-15 01:11:39.404490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db687ad98f56'
down_revision = 'b590f62c7e1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('amcomment', sa.String(length=200), nullable=True))
    op.add_column('events', sa.Column('fmcomment', sa.String(length=200), nullable=True))
    op.add_column('events', sa.Column('pmcomment', sa.String(length=200), nullable=True))
    op.add_column('events', sa.Column('sbcomment', sa.String(length=200), nullable=True))
    op.add_column('events', sa.Column('scscomment', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'scscomment')
    op.drop_column('events', 'sbcomment')
    op.drop_column('events', 'pmcomment')
    op.drop_column('events', 'fmcomment')
    op.drop_column('events', 'amcomment')
    # ### end Alembic commands ###
