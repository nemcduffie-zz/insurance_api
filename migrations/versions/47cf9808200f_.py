"""empty message

Revision ID: 47cf9808200f
Revises: 378fcb075a43
Create Date: 2020-08-17 11:30:26.735964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47cf9808200f'
down_revision = '378fcb075a43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('address', sa.String(length=120), nullable=True))
    op.add_column('users', sa.Column('children', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('email', sa.String(length=120), nullable=True))
    op.add_column('users', sa.Column('name', sa.String(length=80), nullable=True))
    op.add_column('users', sa.Column('num_children', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('occupation', sa.String(length=80), nullable=True))
    op.add_column('users', sa.Column('occupation_type', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'occupation_type')
    op.drop_column('users', 'occupation')
    op.drop_column('users', 'num_children')
    op.drop_column('users', 'name')
    op.drop_column('users', 'email')
    op.drop_column('users', 'children')
    op.drop_column('users', 'address')
    # ### end Alembic commands ###