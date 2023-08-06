# -*- coding: utf-8; -*-
"""add discount.type

Revision ID: fae21d8c854a
Revises: 811f436d593c
Create Date: 2022-02-24 10:24:30.914592

"""

from __future__ import unicode_literals, absolute_import

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fae21d8c854a'
down_revision = '811f436d593c'
branch_labels = None
depends_on = None


def upgrade():

    # transaction_item_discount
    op.add_column('transaction_item_discount', sa.Column('discount_type', sa.String(length=50), nullable=True))


def downgrade():

    # transaction_item_discount
    op.drop_column('transaction_item_discount', 'discount_type')
