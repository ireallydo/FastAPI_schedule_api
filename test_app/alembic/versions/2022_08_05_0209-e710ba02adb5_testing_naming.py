"""testing naming

Revision ID: e710ba02adb5
Revises: 383dd5c35290
Create Date: 2022-08-05 02:09:29.294228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e710ba02adb5'
down_revision = '383dd5c35290'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('test_col', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'test_col')
    # ### end Alembic commands ###
