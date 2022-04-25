"""create post table

Revision ID: 059295a1503f
Revises: 
Create Date: 2022-04-24 10:23:18.381486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '059295a1503f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', 
            sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
            sa.Column('title', sa.String(), nullable=False)
                   )


def downgrade():
    op.drop_table('posts')
