"""empty message

Revision ID: 6d62f943aeda
Revises: 7ce9c51b1f50
Create Date: 2022-03-09 00:52:59.332944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d62f943aeda'
down_revision = '7ce9c51b1f50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=256), nullable=False),
    sa.Column('upload_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('filename')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file')
    # ### end Alembic commands ###
