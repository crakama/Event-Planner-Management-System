"""empty message

Revision ID: 61dbcaa98262
Revises: b6c078fac8df
Create Date: 2017-10-19 15:23:08.653644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61dbcaa98262'
down_revision = 'b6c078fac8df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('remoteusers', sa.Column('is_scsadmin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('remoteusers', 'is_scsadmin')
    # ### end Alembic commands ###
