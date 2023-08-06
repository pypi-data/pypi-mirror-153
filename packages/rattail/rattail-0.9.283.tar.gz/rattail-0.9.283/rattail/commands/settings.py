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
Commands to manage settings
"""

from __future__ import unicode_literals, absolute_import

from rattail import commands


class SettingGet(commands.Subcommand):
    """
    Get a setting value from the DB
    """
    name = 'setting-get'
    description = __doc__.strip()

    def add_parser_args(self, parser):
        parser.add_argument('name', help="Name of the setting to retrieve.")

    def run(self, args):
        session = self.make_session()
        value = self.app.get_setting(session, args.name)
        session.commit()
        session.close()
        self.stdout.write(value)


class SettingPut(commands.Subcommand):
    """
    Add or update a setting in the DB
    """
    name = 'setting-put'
    description = __doc__.strip()

    def add_parser_args(self, parser):
        parser.add_argument('name', help="Name of the setting to save.")
        parser.add_argument('value', help="String value for the setting.")

    def run(self, args):
        session = self.make_session()
        self.app.save_setting(session, args.name, args.value)
        session.commit()
        session.close()
