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
CSV Reports
"""

from __future__ import unicode_literals, absolute_import

import csv

import six

from rattail.reporting import Report
from rattail.csvutil import UnicodeDictWriter


class CSVReport(Report):
    """
    Generic report which knows how to write CSV output file.

    .. attr:: output_fields

       Simple list of field names which should be included in the output file.

    """
    output_fields = []

    def make_filename(self, session, params, data, **kwargs):
        return "{}.csv".format(self.name)

    def get_output_fields(self, params):
        return list(self.output_fields)

    def write_file(self, session, params, data, path, progress=None, **kwargs):
        """
        Write a basic CSV output file with the given data.  Requires
        :attr:`output_fields` attribute to be set to work correctly.
        """
        fields = self.get_output_fields(params)

        if six.PY2:
            csv_file = open(path, 'wb')
            writer = UnicodeDictWriter(csv_file, fields, encoding='utf_8')
        else: # PY3
            csv_file = open(path, 'wt', encoding='utf_8')
            writer = csv.DictWriter(csv_file, fields)

        self.write_file_header(writer)

        def writerow(row, i):
            writer.writerow(row)

        self.progress_loop(writerow, data, progress,
                           message="Generating CSV output")
        csv_file.close()

    def write_file_header(self, writer, **kwargs):
        writer.writeheader()
