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
Products Handler
"""

from __future__ import unicode_literals, absolute_import

import decimal
import warnings
import logging

import six
import sqlalchemy as sa
from sqlalchemy import orm

from rattail import pod
from rattail.db import api
from rattail.util import load_object
from rattail.app import GenericHandler
from rattail.gpc import GPC
from rattail.barcodes import upce_to_upca


log = logging.getLogger(__name__)


class ProductsHandler(GenericHandler):
    """
    Base class and default implementation for product handlers.

    A products handler of course should get the final say in how products are
    handled.  This means everything from pricing, to whether or not a
    particular product can be deleted, etc.
    """

    def make_gpc(self, value, ignore_errors=False, **kwargs):
        """
        Try to convert the given value to a GPC, and return the
        result.

        :param value: Value to be converted.  This should be either a
           string or integer value.

        :param ignore_errors: If ``value`` is not valid for a GPC, an
           error will be raised unless this param is set to true.

        :returns: A :class:`~rattail.gpc.GPC` instance.  Or, if the
           ``value`` is not valid, and ``ignore_errors`` was true,
           then returns ``None``.
        """
        # normalize to string; remove unwanted chars
        if not isinstance(value, six.string_types):
            value = six.text_type(value)
        value = value.replace(' ', '')
        value = value.replace('-', '')

        # auto-handle check digit unless specified
        kwargs.setdefault('calc_check_digit', 'auto')

        try:
            return GPC(value, **kwargs)
        except:
            if not ignore_errors:
                raise

    def make_full_description(self, product=None,
                              brand_name=None, description=None, size=None,
                              **kwargs):
        """
        Return a "full" description for the given product, or
        attributes thereof.

        :param product: Optional, but can be a reference to either a
           :class:`~rattail.db.model.products.Product` or
           :class:`~rattail.db.model.products.PendingProduct`
           instance.

        :param brand_name: Optional; brand name as string.  If not
           provided then will be obtained from ``product`` param.

        :param description: Optional; description as string.  If not
           provided then will be obtained from ``product`` param.

        :param size: Optional; size as string.  If not provided then
           will be obtained from ``product`` param.
        """
        from rattail.db.util import make_full_description

        model = self.model

        if brand_name is None and product:
            if product.brand:
                brand_name = product.brand.name
            elif isinstance(product, model.PendingProduct):
                brand_name = product.brand_name

        if description is None and product:
            description = product.description

        if size is None and product:
            size = product.size

        return make_full_description(brand_name, description, size)

    # TODO: deprecate / remove (afaik it is not being used?)
    def find_products_by_key(self, session, value, **kwargs):
        """
        Locate any products where the "key" matches the given value.

        By default this search is as "thorough" as possible and may
        return multiple results in some cases where you might not
        expect them.  Please pass the ``only`` param if you need a
        more focused search etc.

        :param session: Session for the Rattail database.

        :param value: Value to search for.  Can be a GPC object or
           string.

        :param only: You can optionally direct the logic to search
           only for certain types of keys, by passing a list here,
           e.g.  ``['upc', 'sku']``, or can just pass a single string
           (e.g. ``'upc'``) if only one key is needed.  Otherwise by
           default the logic will search for "all" possible keys.

        :param vendor: You can optionally specify a Vendor, if your
           search needs to include a SKU lookup.  Only matches for
           that vendor will be returned.  Note that by default there
           is no vendor which means "any" SKU might match.

        :param include_keys: You can optionally request that the
           return value include indications of which key was matched,
           for each product result.

        :returns: If ``include_keys`` is true, then will return a list
           of 2-tuples representing each match.  The first element of
           the tuple will be the "key" field pseudonym which was
           matched on; the second element will be the product.

           But if ``include_keys`` is false, then will return just a
           simple list of the products, i.e. won't include the keys.

           Either way of course the list might be empty.
        """
        from rattail.db.api.products import (get_product_by_upc,
                                             get_product_by_item_id,
                                             get_product_by_scancode,
                                             get_product_by_code,
                                             get_product_by_vendor_code)

        model = self.model
        only = kwargs.get('only')
        if isinstance(only, six.string_types):
            only = [only]
        vendor = kwargs.get('vendor')
        include_keys = kwargs.get('include_keys', False)
        products = []

        # don't bother if we're given empty value
        if not value:
            return products

        # TODO: most of the function calls below are only good for "at
        # most one" result.  in some cases there may be more than one
        # match in fact, which will raise an error.  need to refactor
        # somehow to account for that..for now just pass `only` param
        # to avoid the problematic keys for your situation.

        # maybe look for 'uuid' match
        if not only or 'uuid' in only:
            product = session.query(model.Product).get(value)
            if product:
                products.append(('uuid', product))

        # maybe look for 'upc' match
        if not only or 'upc' in only:

            # if value is a GPC we kind of only have one thing to try
            if isinstance(value, GPC):
                product = get_product_by_upc(session, value)
                if product:
                    products.append(('upc', product))

            else: # not GPC, so must convert

                if value.isdigit():

                    # we first assume the value *does* include check digit
                    provided = GPC(value, calc_check_digit=False)
                    product = get_product_by_upc(session, provided)
                    if product:
                        products.append(('upc', product))

                    # but we can also calculate a check digit and try that
                    checked = GPC(value, calc_check_digit='upc')
                    product = get_product_by_upc(session, checked)
                    if product:
                        products.append(('upc', product))

                    # one last trick is to expand UPC-E to UPC-A and then reattempt
                    # the lookup, *with* check digit (since it would be known)
                    if len(value) in (6, 8):
                        checked = GPC(upce_to_upca(value), calc_check_digit='upc')
                        product = get_product_by_upc(session, checked)
                        if product:
                            products.append(('upc', product))

        # maybe look for 'item_id' match
        if not only or 'item_id' in only:
            product = get_product_by_item_id(session, value)
            if product:
                products.append(('item_id', product))

        # maybe look for 'scancode' match
        if not only or 'scancode' in only:
            product = get_product_by_scancode(session, value)
            if product:
                products.append(('scancode', product))

        # maybe look for 'altcode' match
        if not only or 'altcode' in only:
            product = get_product_by_code(session, value)
            if product:
                products.append(('altcode', product))

        # maybe look for 'sku' match
        if not only or 'sku' in only:
            product = get_product_by_vendor_code(session, value,
                                                 vendor=vendor)
            if product:
                products.append(('sku', product))

        # maybe strip keys out of the result
        if not include_keys:
            products = [tup[1] for tup in products]

        return products

    def locate_product_for_entry(self, session, entry, **kwargs):
        """
        This method aims to provide sane default logic for locating a
        :class:`~rattail.db.model.products.Product` record for the
        given "entry" value.

        The default logic here will try to honor the "configured"
        product key field, and prefer that when attempting the lookup.

        :param session: Reference to current DB session.

        :param entry: Value to use for lookup.  This is most often a
           simple string, but the method can handle a few others.  For
           instance it is common to read values from a spreadsheet,
           and sometimes those come through as integers etc.  If this
           value is a :class:`~rattail.gpc.GPC` instance, special
           logic may be used for the lookup.

        :param lookup_fields: Optional list of fields to use for
           lookup.  The default value is ``['uuid', '_product_key_']``
           which means to lookup by UUID as well as "product key"
           field, which is configurable.  You can include any of the
           following in ``lookup_fields``:

           * ``uuid``
           * ``_product_key_`` - :meth:`locate_product_for_key`
           * ``upc`` - :meth:`locate_product_for_upc`
           * ``item_id`` - :meth:`locate_product_for_item_id`
           * ``scancode`` - :meth:`locate_product_for_scancode`
           * ``vendor_code`` - :meth:`locate_product_for_vendor_code`
           * ``alt_code`` - :meth:`locate_product_for_alt_code`

        :returns: First :class:`~rattail.db.model.products.Product`
           instance found if there was a match; otherwise ``None``.
        """
        model = self.model
        if not entry:
            return

        # if entry is GPC then only look for that type of match
        # TODO: is this really the expected behavior?  maybe not..
        if isinstance(entry, GPC):
            return self.locate_product_for_gpc(session, entry)

        # figure out which fields we should match on
        # TODO: let config declare default lookup_fields
        lookup_fields = kwargs.get('lookup_fields', [
            'uuid',
            '_product_key_',
        ])
        if kwargs.get('lookup_vendor_code'): # pragma: no cover
            warnings.warn("`lookup_vendor_code` param is deprecated, "
                          "please include 'vendor_code' in `lookup_fields` "
                          "instead", DeprecationWarning)
            if 'vendor_code' not in lookup_fields:
                lookup_fields.append('vendor_code')
        if kwargs.get('lookup_by_code'): # pragma: no cover
            warnings.warn("`lookup_by_code` param is deprecated, "
                          "please include 'alt_code' in `lookup_fields` "
                          "instead", DeprecationWarning)
            if 'alt_code' not in lookup_fields:
                lookup_fields.append('alt_code')

        # try to locate product by uuid before other, more specific key
        # if kwargs.get('try_uuid', True):
        if 'uuid' in lookup_fields:
            if isinstance(entry, six.string_types):
                product = session.query(model.Product).get(entry)
                if product:
                    return product

        lookups = {
            'uuid': None,
            '_product_key_': self.locate_product_for_key,
            'upc': self.locate_product_for_upc,
            'item_id': self.locate_product_for_item_id,
            'scancode': self.locate_product_for_scancode,
            'vendor_code': self.locate_product_for_vendor_code,
            'alt_code': self.locate_product_for_alt_code,
        }

        for field in lookup_fields:
            if field in lookups:
                lookup = lookups[field]
                if lookup:
                    product = lookup(session, entry, **kwargs)
                    if product:
                        return product
            else:
                log.warning("unknown lookup field: %s", field)

    def locate_product_for_upc(self, session, entry, **kwargs):
        """
        Locate the product which matches the given UPC value.

        This will do a lookup on the
        :attr:`rattail.db.model.products.Product.upc` field only.

        The ``entry`` value provided is expected to be a string, which
        will be coerced to a :class:`~rattail.gpc.GPC` value in
        various ways while attempting the lookup.  If you already have
        a known-good GPC value then you probably should be using
        :meth:`locate_product_for_gpc()` instead.

        Note that instead of calling this method directly, you might
        consider calling :meth:`locate_product_for_key` instead.

        :param session: Current session for Rattail DB.

        :param entry: String value representing the UPC (or EAN13).

        :returns: First :class:`~rattail.db.model.products.Product`
           instance found if there was a match; otherwise ``None``.
        """
        if not entry:
            return

        # assume entry is string; valid only if all digits
        entry = six.text_type(entry)
        if not entry.isdigit():
            return

        # we first assume the user entry *does* include check digit
        provided = self.make_gpc(entry, calc_check_digit=False)
        product = self.locate_product_for_gpc(session, provided, **kwargs)
        if product:
            return product

        # but we can also calculate a check digit and try that
        checked = self.make_gpc(entry, calc_check_digit='upc')
        product = self.locate_product_for_gpc(session, checked, **kwargs)
        if product:
            return product

        # one last trick is to expand UPC-E to UPC-A and then reattempt
        # the lookup, *with* check digit (since it would be known)
        if len(entry) in (6, 8):
            checked = self.make_gpc(upce_to_upca(entry), calc_check_digit='upc')
            product = self.locate_product_for_gpc(session, checked, **kwargs)
            if product:
                return product

    def locate_product_for_item_id(self, session, entry, **kwargs):
        """
        Locate the product which matches the given item ID.

        This will do a lookup on the
        :attr:`rattail.db.model.products.Product.item_id` field only.

        Note that instead of calling this method directly, you might
        consider calling :meth:`locate_product_for_key` instead.

        :param session: Current session for Rattail DB.

        :param entry: Item ID value as string.

        :returns: First :class:`~rattail.db.model.products.Product`
           instance found if there was a match; otherwise ``None``.
        """
        from rattail.db.api.products import get_product_by_item_id

        if not entry:
            return

        # assume entry is string
        entry = six.text_type(entry)

        # do basic lookup
        return get_product_by_item_id(session, entry)

    def locate_product_for_scancode(self, session, entry, **kwargs):
        """
        Locate the product which matches the given scancode.

        This will do a lookup on the
        :attr:`rattail.db.model.products.Product.scancode` field only.

        Note that instead of calling this method directly, you might
        consider calling :meth:`locate_product_for_key` instead.

        :param session: Current session for Rattail DB.

        :param entry: Scancode value as string.

        :returns: First :class:`~rattail.db.model.products.Product`
           instance found if there was a match; otherwise ``None``.
        """
        from rattail.db.api.products import get_product_by_scancode

        if not entry:
            return

        # assume entry is string
        entry = six.text_type(entry)

        # do basic lookup
        return get_product_by_scancode(session, entry)

    def locate_product_for_key(self, session, entry, product_key=None, **kwargs):
        """
        Locate the product which matches the given key value.

        This is an abstraction layer so calling logic need not care
        which product key field is configured.  Under the hood this
        will invoke one of:

        * :meth:`locate_product_for_upc`
        * :meth:`locate_product_for_item_id`
        * :meth:`locate_product_for_scancode`

        This will do a lookup on the product key field only.  It
        normally checks config to determine which field to use for
        product key (via
        :meth:`~rattail.config.RattailConfig.product_key()`), but you
        can override by specifying, e.g.  ``product_key='item_id'``.

        :param session: Current session for Rattail DB.

        :param entry: Key value to use for the lookup.

        :param product_key: Optional key field to use for the lookup.
           If not specified, will be read from config.

        :returns: First :class:`~rattail.db.model.products.Product`
           instance if a match was found; otherwise ``None``.
        """
        # prefer caller-provided key over configured key
        if not product_key:
            product_key = self.config.product_key()

        product = None

        if product_key == 'upc':
            product = self.locate_product_for_upc(session, entry)

        elif product_key == 'item_id':
            product = self.locate_product_for_item_id(session, entry)

        elif product_key == 'scancode':
            product = self.locate_product_for_scancode(session, entry)

        return product

    def locate_product_for_gpc(self, session, gpc, **kwargs):
        """
        Try to locate a product for the given GPC value.

        :param session: Current session for Rattail DB.

        :param gpc: :class:`~rattail.gpc.GPC` instance to match on.

        :returns: First :class:`~rattail.db.model.products.Product`
           instance found if there was a match; otherwise ``None``.
        """
        from rattail.db.api.products import get_product_by_upc

        if not gpc:
            return

        # first we try the normal search
        product = get_product_by_upc(session, gpc)
        if product:
            return product

        # maybe also try special search for "Type 2 UPC"
        if gpc.type2_upc and self.convert_type2_for_gpc_lookup():
            cleaned = self.make_gpc('002{}00000'.format(gpc.data_str[1:6]),
                                    calc_check_digit='upc')
            return get_product_by_upc(session, cleaned)

    def convert_type2_for_gpc_lookup(self):
        return self.config.getbool(
            'rattail', 'products.convert_type2_for_gpc_lookup',
            default=False)

    def locate_product_for_vendor_code(self, session, entry, vendor=None, **kwargs):
        """
        Locate the product which matches the given vendor code.

        This will do a lookup on the
        :attr:`rattail.db.model.products.ProductCost.code` field only.

        :param session: Current session for Rattail DB.

        :param entry: Vendor item code value as string.

        :param vendor: :class:`~rattail.db.model.vendors.Vendor` to
           which to restrict the search.  While technically optional,
           in most cases you should specify the vendor when doing this
           type of lookup.

        :returns: First :class:`~rattail.db.model.products.Product`
           instance found if there was a match; otherwise ``None``.
        """
        model = self.model
        query = session.query(model.Product)\
                       .join(model.ProductCost)\
                       .filter(model.ProductCost.code == entry)

        if vendor:
            query = query.filter(model.ProductCost.vendor == vendor)

        if not kwargs.get('include_deleted'):
            query = query.filter(model.Product.deleted == False)

        products = query.all()
        if products:

            # when multiple matches are found, prefer the unit item
            # TODO: this still seems rather arbitrary, should add more
            # configurable smarts at some point maybe
            if len(products) > 1:
                units = [p for p in products
                         if p.is_unit_item()]
                if units:
                    return units[0]

            return products[0]

    def locate_product_for_alt_code(self, session, entry, **kwargs):
        """
        Locate the product which matches the given alternate code.

        This will do a lookup on the
        :attr:`rattail.db.model.products.ProductCode.code` field only.

        :param session: Current session for Rattail DB.

        :param entry: Alternate code value as string.

        :returns: First :class:`~rattail.db.model.products.Product`
           instance found if there was a match; otherwise ``None``.
        """
        from rattail.db.api.products import get_product_by_code

        return get_product_by_code(session, entry)

    def normalize_product(self, product, fields=None, **kwargs):
        """
        Normalize the given product to a JSON-serializable dict.
        """
        data = {
            'uuid': product.uuid,
            'product_key': self.render_product_key(product),
            'description': product.description,
            'size': product.size,
        }

        if not fields:
            fields = [
                'brand_name',
                'full_description',
                'department_name',
            ]

        if 'url' in fields:
            data['url'] = self.get_url(product)

        if 'image_url' in fields:
            data['image_url'] = self.get_image_url(product)

        if 'brand_name' in fields:
            data['brand_name'] = product.brand.name if product.brand else None

        if 'full_description' in fields:
            data['full_description'] = self.make_full_description(product)

        if 'department_name' in fields:
            data['department_name'] = product.department.name if product.department else None

        if 'unit_price_display' in fields:
            data['unit_price_display'] = self.render_price(product.regular_price)

        if 'vendor_name' in fields:
            vendor = product.cost.vendor if product.cost else None
            data['vendor_name'] = vendor.name if vendor else None

        sale_fields = [
            'sale_price',
            'sale_price_display',
            'sale_ends',
            'sale_ends_display',
            'case_price',
            'case_price_display',
        ]
        if any([f in fields for f in sale_fields]):
            sale_price = None
            if not product.not_for_sale:
                sale_price = product.current_price
                if sale_price:
                    if sale_price.price:
                        data['sale_price'] = float(sale_price.price)
                    data['sale_price_display'] = self.render_price(sale_price)
                    sale_ends = sale_price.ends
                    if sale_ends:
                        sale_ends = self.app.localtime(sale_ends, from_utc=True).date()
                        data['sale_ends'] = six.text_type(sale_ends)
                        data['sale_ends_display'] = self.app.render_date(sale_ends)

        if 'case_quantity' in fields:
            data['case_quantity'] = self.app.render_quantity(
                self.get_case_size(product))

        if 'case_price' in fields or 'case_price_display' in fields:
            case_price = None
            if product.regular_price and product.regular_price is not None:
                case_size = self.get_case_size(product)
                # use sale price if there is one, else normal unit price
                unit_price = product.regular_price.price
                if sale_price:
                    unit_price = sale_price.price
                case_price = (case_size or 1) * unit_price
                case_price = case_price.quantize(decimal.Decimal('0.01'))
            data['case_price'] = six.text_type(case_price) if case_price is not None else None
            data['case_price_display'] = self.app.render_currency(case_price)

        if 'uom_choices' in fields:
            data['uom_choices'] = self.get_uom_choices(product)

        return data

    def get_uom_choices(self, product=None, **kwargs):
        """
        Return a list of UOM choices for the given product, or if no
        product specified then should return the default choices.
        """
        choices = []

        # TODO: not sure how generically useful this method even is? i
        # think it is only used when making a new custorder so far..

        # TODO: for instance "pound" vs. "each" is really just 2 ways
        # of saying "unit" - and does not consider i18n etc.

        # Each
        if not product or not product.weighed:
            unit_name = self.enum.UNIT_OF_MEASURE[self.enum.UNIT_OF_MEASURE_EACH]
            choices.append({'key': self.enum.UNIT_OF_MEASURE_EACH,
                            'value': unit_name})

        # # Pound
        # if not product or product.weighed:
        #     unit_name = self.enum.UNIT_OF_MEASURE[self.enum.UNIT_OF_MEASURE_POUND]
        #     choices.append({
        #         'key': self.enum.UNIT_OF_MEASURE_POUND,
        #         'value': unit_name,
        #     })

        # Case
        case_text = None
        case_size = None
        if product:
            case_size = self.get_case_size(product)
        if case_size is None:
            case_text = "{} (&times; ?? {})".format(
                self.enum.UNIT_OF_MEASURE[self.enum.UNIT_OF_MEASURE_CASE],
                unit_name)
        elif case_size > 1:
            case_text = "{} (&times; {} {})".format(
                self.enum.UNIT_OF_MEASURE[self.enum.UNIT_OF_MEASURE_CASE],
                self.app.render_quantity(case_size),
                unit_name)
        if case_text:
            choices.append({'key': self.enum.UNIT_OF_MEASURE_CASE,
                            'value': case_text})

        return choices

    def get_case_size(self, product):
        """
        Return the effective case size for the given product.
        """
        if product.case_size:
            return product.case_size

        cost = product.cost
        if cost:
            return cost.case_size

    def get_url(self, product, **kwargs):
        """
        Return the Tailbone "view" URL for the given product.
        """
        base_url = self.config.base_url()
        if base_url:
            return '{}/products/{}'.format(base_url, product.uuid)

    def get_image_url(self, product=None, upc=None, **kwargs):
        """
        Return the preferred image URL for the given UPC or product.
        """
        base_url = self.config.base_url()

        # we prefer the "image on file" if available
        if base_url and product and product.image:
            return '{}/products/{}/image'.format(base_url, product.uuid)

        # and if this product is a pack item, then we prefer the unit
        # item image as fallback, if available
        if base_url and product and product.is_pack_item():
            unit = product.unit
            if unit and unit.image:
                return '{}/products/{}/image'.format(base_url, unit.uuid)

        # fallback to the POD image, if available and so configured
        if self.config.getbool('tailbone', 'products.show_pod_image',
                               default=False):
            if product and not upc:
                upc = product.upc
            if upc:
                return self.get_pod_image_url(upc)

        if base_url:
            return '{}/tailbone/img/product.png'.format(base_url)

    def get_pod_image_url(self, upc, **kwargs):
        """
        Return the POD image URL for the given UPC.
        """
        if upc:
            return pod.get_image_url(self.config, upc)

    def render_product_key(self, product, **kwargs):
        """
        Render the key value for the given product, as human-readable
        text.
        """
        product_key = self.config.product_key()
        if product_key == 'upc':
            return self.app.render_gpc(product.upc)
        return six.text_type(getattr(product, product_key))

    def render_price(self, price, html=False, **kwargs):
        """
        Render the given ``price`` object as text.

        :returns: String containing the rendered price, or ``None`` if
           nothing was applicable.
        """
        if not price:
            return ""
        if price.price is not None and price.pack_price is not None:
            if price.multiple > 1:
                return "{} / {}  ({} / {})".format(
                    self.app.render_currency(price.price),
                    price.multiple,
                    self.app.render_currency(price.pack_price),
                    price.pack_multiple)
            return "{}  ({} / {})".format(
                self.app.render_currency(price.price),
                self.app.render_currency(price.pack_price),
                price.pack_multiple)
        if price.price is not None:
            if price.multiple is not None and price.multiple > 1:
                return "{} / {}".format(
                    self.app.render_currency(price.price),
                    price.multiple)
            return self.app.render_currency(price.price)
        if price.pack_price is not None:
            return "{} / {}".format(
                self.app.render_currency(price.pack_price),
                price.pack_multiple)

    def make_pending_product(self, **kwargs):
        """
        Create and return a new
        :class:`~rattail.db.model.products.PendingProduct` instance,
        per the given kwargs.
        """
        model = self.model
        kwargs.setdefault('status_code', self.enum.PENDING_PRODUCT_STATUS_PENDING)
        pending = model.PendingProduct(**kwargs)
        return pending

    def resolve_product(self, pending, product, user, **kwargs):
        """
        Resolve a pending product.

        :param pending: Reference to a PendingProduct instance.

        :param product: Reference to a Product instance.

        :param user: Reference to the User responsible.
        """
        custorder_handler = self.app.get_custorder_handler()
        custorder_handler.resolve_product(pending, product, user)

        pending.status_code = self.enum.PENDING_PRODUCT_STATUS_RESOLVED

    def get_uom_sil_codes(self, session, uppercase=False, **kwargs):
        """
        This should return a dict, keys of which are UOM abbreviation strings,
        and values of which are corresponding SIL code strings.

        :param session: Reference to current Rattail DB session.
        :param uppercase: Set to ``True`` to cause all UOM abbreviations to be
           upper-cased when adding to the map.
        :returns: Dictionary containing all known UOM / SIL code mappings.
        """
        model = self.model

        def normalize(uom):
            if uom.sil_code:
                return uom.sil_code

        def make_key(uom, normal):
            key = uom.abbreviation
            if uppercase:
                key = key.upper()
            return key

        return self.app.cache_model(session,
                                    model.UnitOfMeasure,
                                    normalizer=normalize,
                                    key=make_key)

    def get_uom_sil_code(self, session, uom, uppercase=False, **kwargs):
        """
        This should return a SIL code which corresponds to the given UOM
        abbreviation string.  Useful when you just need one out of the blue,
        but if you need multiple codes looked up then you're probably better
        off using :meth:`get_uom_sil_codes()` for efficiency.

        :param session: Reference to current Rattail DB session.
        :param uppercase: Set to ``True`` to cause the UOM abbreviation to be
           upper-cased before performing the lookup.  This effectively makes
           the search case-insensitive.
        :param uom:  Unit of measure as abbreviated string, e.g. ``'LB'``.
        :returns: SIL code for the UOM, as string (e.g. ``'49'``), or ``None``
           if no matching code was found.
        """
        model = self.model
        query = session.query(model.UnitOfMeasure)
        if uppercase:
            query = query.filter(sa.func.upper(model.UnitOfMeasure.abbreviation) == uom.upper())
        else:
            query = query.filter(model.UnitOfMeasure.abbreviation == uom)
        try:
            match = query.one()
        except orm.exc.NoResultFound:
            pass
        else:
            return match.sil_code

    def collect_wild_uoms(self, **kwargs):
        """
        Collect all UOM abbreviations "from the wild" and ensure each is
        represented within the Rattail Units of Measure table.

        Note that you should not need to override this method.  Please override
        :meth:`find_wild_uoms()` instead.
        """
        session = self.make_session()
        model = self.model

        wild_uoms = self.find_wild_uoms(session, **kwargs)

        known_uoms = self.app.cache_model(session,
                                          model.UnitOfMeasure,
                                          key='abbreviation')

        for wild_uom in wild_uoms:
            if wild_uom not in known_uoms:
                uom = model.UnitOfMeasure()
                uom.abbreviation = wild_uom
                session.add(uom)

        session.commit()
        session.close()

    def find_wild_uoms(self, session, **kwargs):
        """
        Query some database(s) in order to discover all UOM abbreviations which
        exist "in the wild".

        You are encouraged to override this method as needed.  Note that
        certain POS integration packages may provide some common logic which
        may be used for this.

        :param session: Reference to current Rattail DB session.

        :returns: A list of strings, e.g. ``['OZ', 'LB', ...]``.
        """
        return []


def get_products_handler(config, **kwargs):
    """
    Create and return the configured :class:`ProductsHandler` instance.
    """
    spec = config.get('rattail', 'products.handler')
    if spec:
        factory = load_object(spec)
    else:
        factory = ProductsHandler
    return factory(config, **kwargs)
