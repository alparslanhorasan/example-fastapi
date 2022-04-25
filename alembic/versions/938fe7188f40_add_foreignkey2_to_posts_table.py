"""add foreignkey2 to posts table

Revision ID: 938fe7188f40
Revises: 860bcb1e5243
Create Date: 2022-04-24 13:20:20.273275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '938fe7188f40'
down_revision = '860bcb1e5243'
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
