# -*- coding: utf-8; -*-
"""add patronage

Revision ID: c3b721c34f4b
Revises: 08dcf4eebe66
Create Date: 2022-02-18 18:06:06.533616

"""

from __future__ import unicode_literals, absolute_import

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3b721c34f4b'
down_revision = '08dcf4eebe66'
branch_labels = None
depends_on = None


def upgrade():

    # transaction
    op.add_column('transaction', sa.Column('patronage', sa.Numeric(precision=9, scale=2), nullable=True))
    op.add_column('transaction', sa.Column('equity_current', sa.Boolean(), nullable=True))
    op.add_column('transaction', sa.Column('self_updated', sa.Boolean(), nullable=True))


def downgrade():

    # transaction
    op.drop_column('transaction', 'self_updated')
    op.drop_column('transaction', 'equity_current')
    op.drop_column('transaction', 'patronage')
