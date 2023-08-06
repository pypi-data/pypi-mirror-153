# -*- coding: utf-8; -*-
"""add item discounts

Revision ID: 811f436d593c
Revises: c3b721c34f4b
Create Date: 2022-02-19 15:27:24.452125

"""

from __future__ import unicode_literals, absolute_import

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '811f436d593c'
down_revision = 'c3b721c34f4b'
branch_labels = None
depends_on = None


def upgrade():

    # transaction_item_discount
    op.create_table('transaction_item_discount',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('item_uuid', sa.String(length=32), nullable=False),
                    sa.Column('sequence', sa.Integer(), nullable=False),
                    sa.Column('description', sa.String(length=50), nullable=False),
                    sa.Column('amount', sa.Numeric(precision=9, scale=2), nullable=False),
                    sa.ForeignKeyConstraint(['item_uuid'], ['transaction_item.uuid'], name='transaction_item_discount_fk_item'),
                    sa.PrimaryKeyConstraint('uuid')
    )


def downgrade():

    # transaction_item_discount
    op.drop_table('transaction_item_discount')
