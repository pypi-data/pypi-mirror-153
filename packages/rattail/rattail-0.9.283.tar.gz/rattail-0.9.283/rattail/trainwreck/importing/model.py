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
Trainwreck model importers
"""

from __future__ import unicode_literals, absolute_import

from collections import namedtuple

from sqlalchemy import orm

from rattail import importing
from .util import ToOrFromTrainwreck


Discount = namedtuple('Discount', ['discount_type', 'description', 'amount'])


class ToTrainwreck(ToOrFromTrainwreck, importing.ToSQLAlchemy):
    """
    Base class for all Trainwreck model importers
    """
    key = 'uuid'


class TransactionImporter(ToTrainwreck):
    """
    Transaction data importer

    .. attribute:: match_on_time_field

       This time field will be used for the cache query etc.  In
       particular it controls which transactions are deemed to belong
       to a given date, which is needed when restricting the import to
       a particular date range.  Can set this to ``'upload_time'`` or
       ``'start_time'`` if necessary, depending on the nature of
       transaction data coming from the host side.
    """
    match_on_time_field = 'end_time'

    @property
    def importing_from_system(self):
        raise NotImplementedError("TODO: please define this for your subclass")

    def get_model_class(self):
        if hasattr(self, 'model_class') and self.model_class:
            return self.model_class
        trainwreck = self.config.get_trainwreck_model()
        return trainwreck.Transaction

    def cache_query(self):
        query = super(TransactionImporter, self).cache_query()
        try:
            system = self.importing_from_system
        except NotImplementedError:
            pass
        else:
            query = query.filter(self.model_class.system == system)
        time_field = getattr(self.model_class, self.match_on_time_field)
        return query.filter(time_field >= self.app.make_utc(self.start_time))\
                    .filter(time_field < self.app.make_utc(self.end_time))


class TransactionOrderMarkerImporter(ToTrainwreck):
    """
    Transaction order marker data importer

    .. attribute:: match_on_time_field

       This time field will be used for the cache query etc.  In
       particular it controls which transactions are deemed to belong
       to a given date, which is needed when restricting the import to
       a particular date range.  Can set this to ``'upload_time'`` or
       ``'start_time'`` if necessary, depending on the nature of
       transaction data coming from the host side.
    """
    match_on_time_field = 'end_time'

    @property
    def importing_from_system(self):
        raise NotImplementedError("TODO: please define this for your subclass")

    def get_model_class(self):
        if hasattr(self, 'model_class') and self.model_class:
            return self.model_class
        trainwreck = self.config.get_trainwreck_model()
        return trainwreck.TransactionOrderMarker

    @property
    def transaction_class(self):
        trainwreck = self.config.get_trainwreck_model()
        return trainwreck.Transaction

    def cache_query(self):
        query = super(TransactionOrderMarkerImporter, self).cache_query()
        trainwreck = self.config.get_trainwreck_model()

        query = query.join(trainwreck.Transaction)

        try:
            system = self.importing_from_system
        except NotImplementedError:
            pass
        else:
            query = query.filter(trainwreck.Transaction.system == system)

        time_field = getattr(trainwreck.Transaction, self.match_on_time_field)
        query = query.filter(time_field >= self.app.make_utc(self.start_time))\
                     .filter(time_field < self.app.make_utc(self.end_time))
        return query


class TransactionItemImporter(ToTrainwreck):
    """
    Transaction item data importer

    .. attribute:: match_on_time_field

       This time field will be used for the cache query etc.  In
       particular it controls which transactions are deemed to belong
       to a given date, which is needed when restricting the import to
       a particular date range.  Can set this to ``'upload_time'`` or
       ``'start_time'`` if necessary, depending on the nature of
       transaction data coming from the host side.
    """
    match_on_time_field = 'end_time'

    @property
    def supported_fields(self):
        fields = super(TransactionItemImporter, self).supported_fields
        fields = list(fields)
        fields.extend([
            'transaction_system_id',
            'discounts',
        ])
        return fields

    @property
    def importing_from_system(self):
        raise NotImplementedError("TODO: please define this for your subclass")

    def get_model_class(self):
        if hasattr(self, 'model_class') and self.model_class:
            return self.model_class
        trainwreck = self.config.get_trainwreck_model()
        return trainwreck.TransactionItem

    @property
    def transaction_class(self):
        trainwreck = self.config.get_trainwreck_model()
        return trainwreck.Transaction

    def setup(self):
        super(TransactionItemImporter, self).setup()

        if 'transaction_system_id' in self.fields:
            trainwreck = self.config.get_trainwreck_model()
            query = self.session.query(trainwreck.Transaction)
            try:
                system = self.importing_from_system
            except NotImplementedError:
                pass
            else:
                query = query.filter(trainwreck.Transaction.system == system)

            time_field = getattr(trainwreck.Transaction, self.match_on_time_field)
            query = query.filter(time_field >= self.app.make_utc(self.start_time))\
                         .filter(time_field < self.app.make_utc(self.end_time))
            self.transactions_by_system_id = self.cache_model(trainwreck.Transaction,
                                                              query=query,
                                                              key='system_id')

    def cache_query(self):
        query = super(TransactionItemImporter, self).cache_query()
        trainwreck = self.config.get_trainwreck_model()

        query = query.join(trainwreck.Transaction)

        try:
            system = self.importing_from_system
        except NotImplementedError:
            pass
        else:
            query = query.filter(trainwreck.Transaction.system == system)

        time_field = getattr(trainwreck.Transaction, self.match_on_time_field)
        query = query.filter(time_field >= self.app.make_utc(self.start_time))\
                     .filter(time_field < self.app.make_utc(self.end_time))

        if 'discounts' in self.fields:
            query = query.options(orm.joinedload(trainwreck.TransactionItem.discounts))

        return query

    def normalize_local_object(self, item):
        data = super(TransactionItemImporter, self).normalize_local_object(item)
        if not data:
            return

        if 'transaction_system_id' in self.fields:
            data['transaction_system_id'] = item.transaction.system_id

        if 'discounts' in self.fields:
            data['discounts'] = [Discount(d.discount_type, d.description, d.amount)
                                 for d in item.discounts]

        return data

    def get_transaction_by_system_id(self, system_id):
        if hasattr(self, 'transactions_by_system_id'):
            return self.transactions_by_system_id.get(system_id)

        trainwreck = self.config.get_trainwreck_model()
        query = self.session.query(trainwreck.Transaction)\
                            .filter(trainwreck.Transaction.system_id == system_id)
        try:
            system = self.importing_from_system
        except NotImplementedError:
            pass
        else:
            query = query.filter(trainwreck.Transaction.system == system)
        try:
            return query.one()
        except orm.exc.NoResultFound:
            pass

    def create_object(self, key, host_data):
        item = super(TransactionItemImporter, self).create_object(key, host_data)
        if item:

            # we may have to explicitly assign the transaction, if that uuid
            # wasn't part of our key
            # TODO: actually we do this if system_id was part of the key and do
            # not really look at uuid.  is there a better way to do or explain?
            # TODO: this also may fail outright if we get a bad system_id etc.
            if 'transaction_system_id' in self.key:
                system_id = host_data['transaction_system_id']
                txn = self.get_transaction_by_system_id(system_id)
                if not txn:
                    raise RuntimeError("transaction not found for system_id: {}".format(system_id))
                item.transaction = txn

            return item

    def update_object(self, item, host_data, local_data=None, **kwargs):
        item = super(TransactionItemImporter, self).update_object(
            item, host_data, local_data=local_data, **kwargs)
        if not item:
            return

        if 'discounts' in self.fields:
            trainwreck = self.config.get_trainwreck_model()
            if host_data['discounts']:
                if not local_data or local_data['discounts'] != host_data['discounts']:
                    # TODO: is this too heavy-handed?
                    # just rebuild the line item's "other" discount list,
                    # instead of trying to reconcile the host vs. local lists
                    if item.discounts:
                        del item.discounts[:]
                    for disc in host_data['discounts']:
                        item.discounts.append(
                            trainwreck.TransactionItemDiscount(
                                discount_type=disc.discount_type,
                                description=disc.description,
                                amount=disc.amount))
            else:
                if local_data and local_data['discounts']:
                    del item.discounts[:]
        return item


class TransactionItemDiscountImporter(ToTrainwreck):
    """
    Transaction item discount data importer

    .. attribute:: match_on_time_field

       This time field will be used for the cache query etc.  In
       particular it controls which transactions are deemed to belong
       to a given date, which is needed when restricting the import to
       a particular date range.  Can set this to ``'upload_time'`` or
       ``'start_time'`` if necessary, depending on the nature of
       transaction data coming from the host side.
    """
    match_on_time_field = 'end_time'

    @property
    def importing_from_system(self):
        raise NotImplementedError("TODO: please define this for your subclass")

    def get_model_class(self):
        if hasattr(self, 'model_class') and self.model_class:
            return self.model_class
        trainwreck = self.config.get_trainwreck_model()
        return trainwreck.TransactionItemDiscount

    def cache_query(self):
        query = super(TransactionItemDiscountImporter, self).cache_query()
        trainwreck = self.config.get_trainwreck_model()

        query = query.join(trainwreck.TransactionItem)\
                     .join(trainwreck.Transaction)

        try:
            system = self.importing_from_system
        except NotImplementedError:
            pass
        else:
            query = query.filter(trainwreck.Transaction.system == system)

        time_field = getattr(trainwreck.Transaction, self.match_on_time_field)
        query = query.filter(time_field >= self.app.make_utc(self.start_time))\
                     .filter(time_field < self.app.make_utc(self.end_time))

        return query
