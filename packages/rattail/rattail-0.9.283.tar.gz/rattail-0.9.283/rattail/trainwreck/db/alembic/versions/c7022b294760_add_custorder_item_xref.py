# -*- coding: utf-8; -*-
"""add custorder_item_xref

Revision ID: c7022b294760
Revises: fae21d8c854a
Create Date: 2022-03-16 22:02:04.370686

"""

from __future__ import unicode_literals, absolute_import

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7022b294760'
down_revision = 'fae21d8c854a'
branch_labels = None
depends_on = None


def upgrade():

    # transaction_order_marker
    op.create_table('transaction_order_marker',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('transaction_uuid', sa.String(length=32), nullable=False),
                    sa.Column('custorder_xref', sa.String(length=50), nullable=True),
                    sa.Column('custorder_item_xref', sa.String(length=50), nullable=True),
                    sa.ForeignKeyConstraint(['transaction_uuid'], ['transaction.uuid'], name='transaction_order_marker_fk_transaction'),
                    sa.PrimaryKeyConstraint('uuid')
    )

    # transaction_item
    op.add_column('transaction_item', sa.Column('custorder_item_xref', sa.String(length=50), nullable=True))


def downgrade():

    # transaction_item
    op.drop_column('transaction_item', 'custorder_item_xref')

    # transaction_order_marker
    op.drop_table('transaction_order_marker')
