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
Problem Reports for mailmon
"""

from __future__ import unicode_literals, absolute_import

import six

from rattail.problems import RattailProblemReport
from rattail.mailmon import MailmonConnection
from rattail.mailmon.config import load_mailmon_profiles


class MailmonMisses(RattailProblemReport):
    """
    Looks for any mail in IMAP accounts which appears to have been
    missed by the mailmon daemon.
    """
    problem_key = 'mailmon_misses'
    problem_title = "Mailmon misses"

    def find_problems(self, **kwargs):
        problems = []

        # loop thru all accounts
        monitored = load_mailmon_profiles(self.config)
        for account in six.itervalues(monitored['__accounts__']):
            cxn = MailmonConnection(self.config, account)
            cxn.connect()

            # loop thru all profiles for the account
            for profile in account.monitored:
                count = cxn.select_folder(profile.imap_folder)
                if count:
                    problems.append((account, profile, count))

            cxn.disconnect()

        return problems
