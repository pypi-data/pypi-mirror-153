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
Global Product Code
"""

from __future__ import unicode_literals, absolute_import

import six

from rattail import barcodes


@six.python_2_unicode_compatible
class GPC(object):
    """
    Class to abstract the details of Global Product Code data.  Examples of
    this would be UPC or EAN barcodes.

    The initial motivation for this class was to provide better SIL support.
    To that end, the instances are assumed to always be comprised of only
    numeric digits, and must include a check digit.  If you do not know the
    check digit, provide a ``calc_check_digit`` value to the constructor.

    :param value: Must be either an integer or a long value, or (most
       commonly) a string containing only digits.

    :param calc_check_digit: Controls if/how check digit should be
       calculated.

       Default is ``False`` which means do not calculate a check
       digit (i.e. assume it is already present in ``value``).

       You can specify the string ``'upc'`` to force calculation
       of check digit using the standard UPC algorithm.

       Or specify the string ``'auto'`` to invoke automagic logic
       which tries to guess whether or not the given value has/needs a
       check digit.  Please note, this is not fool-proof so you should
       avoid if possible.

    ..
       :param from_upce: Flag indicating whether the ``value`` is in
          UPC-E format.  If ``True`` then the value will be automatically
          converted to UPC-A format before constructing the GPC.  If
          ``False`` then the value will be left as-is and not assumed to
          be UPC-E format.  Note that this flag defaults to ``None``
          which means effectively that you do not know whether value is
          UPC-E, and so the constructor should guess.
    """

    def __init__(self, value, calc_check_digit=False):
        value = six.text_type(value)

        if calc_check_digit == 'auto':
            calc_check_digit = 'upc' if len(value) < 12 else False

        if calc_check_digit is True or calc_check_digit == 'upc':
            value += six.text_type(barcodes.upc_check_digit(value))

        self.value = int(value)

    def __eq__(self, other):
        try:
            return int(self) == int(other)
        except (TypeError, ValueError):
            return False

    def __ne__(self, other):
        try:
            return int(self) != int(other)
        except (TypeError, ValueError):
            return True

    # TODO: this is no longer used in python3
    # https://docs.python.org/3/whatsnew/3.0.html#ordering-comparisons
    # TODO: need to implement "rich comparisons" instead
    # https://docs.python.org/3/reference/datamodel.html#object.__lt__
    def __cmp__(self, other):

        # treat non-integers as being less than myself
        try:
            other = int(other)
        except (TypeError, ValueError):
            return 1

        myself = int(self)
        if myself < other:
            return -1
        if myself > other:
            return 1
        assert myself == other
        return 0

    def __lt__(self, other):
        try:
            return int(self) < int(other)
        except (TypeError, ValueError):
            return False

    def __hash__(self):
        return hash(self.value)

    def __int__(self):
        return int(self.value)

    def __long__(self):
        return long(self.value)

    def __repr__(self):
        return "GPC('%014d')" % self.value

    def __str__(self):
        # return str('%14d' % self.value)
        return str('{:014d}'.format(self.value))

    @property
    def data_str(self):
        """
        Returns the "data" for the barcode as unicode string, i.e. minus check
        digit and also with all leading zeroes removed.  A visual is maybe
        helpful here::

           >>> upc = GPC('7430500132', calc_check_digit='upc')
           >>> print(repr(upc))
           GPC('00074305001321')
           >>> print(repr(upc.data_str))
           u'7430500132'

        Note that in this case the ``data_str`` value is the same as was
        originally provided to the constructor, but that isn't always the case.
        """
        return six.text_type(int(self))[:-1]

    @property
    def data_length(self):
        """
        Returns the length of the "data" for the barcode.  This is just a
        convenience that returns ``len(self.data_str)``.
        """
        return len(self.data_str)

    @property
    def type2_upc(self):
        """
        Returns boolean indicating whether the barcode has "type 2" UPC data.
        """
        return self.data_str.startswith('2') and self.data_length == 11

    def pretty(self):
        """
        Returns the UPC as a somewhat more human-readable string.  Basically
        that just means the check digit is distinguished by a hyphen.
        """
        upc = six.text_type(self)
        return "{0}-{1}".format(upc[:-1], upc[-1])
