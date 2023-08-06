# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2022 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
TrainWreck -> "self" data importing
"""

from __future__ import unicode_literals, absolute_import

from sqlalchemy import orm

from rattail import importing
from rattail.trainwreck.importing.trainwreck import FromTrainwreckHandler
from rattail.trainwreck import importing as trainwreck_importing


class FromTrainwreckToSelf(FromTrainwreckHandler, importing.ToSQLAlchemyHandler):
    """
    Base handler class for Trainwreck -> "self"
    """
    host_key = 'self'
    host_title = "Trainwreck (self)"
    generic_host_title = "Trainwreck (self)"

    local_key = 'trainwreck'
    local_title = "Trainwreck (self)"
    generic_local_title = "Trainwreck (self)"

    def begin_local_transaction(self):
        self.session = self.host_session

    def rollback_transaction(self):
        self.rollback_host_transaction()

    def commit_transaction(self):
        self.commit_host_transaction()


class FromTrainwreck(importing.FromSQLAlchemy):
    """
    Common base class for the "host" side of importers which read data
    from the Trainwreck DB for the sake of updating misc. other tables
    in that same DB.
    """


class TransactionImporter(FromTrainwreck, trainwreck_importing.model.TransactionImporter):
    """
    Base class for Trainwreck -> "self" for Transaction model.
    """
    allow_create = False
    allow_delete = False

    @property
    def host_model_class(self):
        trainwreck = self.config.get_trainwreck_model()
        return trainwreck.Transaction

    def query(self):
        query = super(TransactionImporter, self).query()
        trainwreck = self.config.get_trainwreck_model()

        time_field = getattr(trainwreck.Transaction, self.match_on_time_field)
        query = query.filter(time_field >= self.app.make_utc(self.start_time))\
                     .filter(time_field < self.app.make_utc(self.end_time))

        query = query.options(orm.joinedload(trainwreck.Transaction.items)\
                              .joinedload(trainwreck.TransactionItem.discounts))

        return query

    def normalize_host_object(self, txn):
        """
        This method is defined only as a convenience for the simple
        case where you need to mark a transaction as having been
        updated, along with some other "processing" logic.
        """
        return {
            'uuid': txn.uuid,
            'self_updated': True,
        }
