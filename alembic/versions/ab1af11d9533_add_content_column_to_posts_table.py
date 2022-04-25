"""add content column to posts table

Revision ID: ab1af11d9533
Revises: 059295a1503f
Create Date: 2022-04-24 11:34:02.023343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab1af11d9533'
down_revision = '059295a1503f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade():
    op.drop_column('posts','content')
