"""add last few columns-2 to posts table

Revision ID: be6d5227815d
Revises: 6389f67b9dc2
Create Date: 2022-04-24 13:46:54.083840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be6d5227815d'
down_revision = '6389f67b9dc2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', 
                        sa.Column('published', sa.Boolean(), 
                        nullable=False, server_default='TRUE')
                 )
    op.add_column('posts', 
                        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                        server_default=sa.text('now()'),
                        nullable=False)
                 )


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
