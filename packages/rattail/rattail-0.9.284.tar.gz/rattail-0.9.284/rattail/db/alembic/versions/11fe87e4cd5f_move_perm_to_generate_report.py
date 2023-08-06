# -*- coding: utf-8; -*-
"""move perm to generate report

Revision ID: 11fe87e4cd5f
Revises: d8b0ba4fa795
Create Date: 2022-01-31 19:18:22.274391

"""

from __future__ import unicode_literals, absolute_import

# revision identifiers, used by Alembic.
revision = '11fe87e4cd5f'
down_revision = u'd8b0ba4fa795'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types


permission = sa.sql.table('permission', sa.sql.column('permission'))

def rename_perm(oldname, newname):
    op.execute(permission.update()\
               .where(permission.c.permission == oldname)\
               .values({'permission': newname}))


def upgrade():
    rename_perm('report_output.generate', 'report_output.create')


def downgrade():
    rename_perm('report_output.create', 'report_output.generate')
