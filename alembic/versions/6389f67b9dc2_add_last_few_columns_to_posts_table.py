"""add last few columns to posts table

Revision ID: 6389f67b9dc2
Revises: 938fe7188f40
Create Date: 2022-04-24 13:31:28.638651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6389f67b9dc2'
down_revision = '938fe7188f40'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), 
                        nullable=False,server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', 
                           sa.TIMESTAMP(timezone=True),
                           server_default=sa.text('now()'), nullable=False))


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
