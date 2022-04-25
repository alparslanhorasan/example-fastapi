"""add users table

Revision ID: 995661b5ca5b
Revises: ab1af11d9533
Create Date: 2022-04-24 12:21:38.914581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '995661b5ca5b'
down_revision = 'ab1af11d9533'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
            sa.Column('id', sa.Integer(), nullable=False), 
            sa.Column('email', sa.String(), nullable=False),
            sa.Column('password', sa.String(), nullable=False),
            sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                        server_default=sa.text('now()'), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email')     
                   )
def downgrade():
    op.drop_table('users')
