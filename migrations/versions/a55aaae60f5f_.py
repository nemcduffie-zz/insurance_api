"""empty message

Revision ID: a55aaae60f5f
Revises: 47cf9808200f
Create Date: 2020-08-27 08:02:58.540837

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a55aaae60f5f'
down_revision = '47cf9808200f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('revoked_tokens')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('revoked_tokens',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('jti', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='revoked_tokens_pkey')
    )
    # ### end Alembic commands ###
