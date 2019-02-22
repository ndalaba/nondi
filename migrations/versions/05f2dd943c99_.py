"""empty message

Revision ID: 05f2dd943c99
Revises: d165f1b03305
Create Date: 2019-02-22 10:26:38.184511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05f2dd943c99'
down_revision = 'd165f1b03305'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('videos', sa.Column('description', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('videos', 'description')
    # ### end Alembic commands ###
