"""add foreignkey to posts table

Revision ID: 860bcb1e5243
Revises: 995661b5ca5b
Create Date: 2022-04-24 12:54:33.087614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '860bcb1e5243'
down_revision = '995661b5ca5b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts",
    referent_table="users", local_cols=['owner_id'], remote_cols=['id'],
    ondelete="CASCADE")

def downgrade():
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts','owner_id')
