"""Handwritten migration

Revision ID: db0ae06097d4
Revises: e710ba02adb5
Create Date: 2022-08-06 19:02:38.403329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db0ae06097d4'
down_revision = 'e710ba02adb5'
branch_labels = None
depends_on = None

# this is a handwritten migration 

def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
