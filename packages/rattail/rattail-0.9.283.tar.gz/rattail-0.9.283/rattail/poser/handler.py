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
Poser Handler
"""

from __future__ import unicode_literals, absolute_import

import os
import sys
import subprocess
import logging

import six
from mako.lookup import TemplateLookup

from rattail.app import GenericHandler
from rattail.files import resource_path
from rattail.util import import_module_path, import_reload, OrderedDict, simple_error
from rattail.reporting import ExcelReport
from rattail.config import ConfigExtension


log = logging.getLogger(__name__)


class PoserHandler(GenericHandler):
    """
    Base class and default implementation for Poser (custom code)
    handler.
    """

    def sanity_check(self):
        poserdir = self.get_default_poser_dir()
        return os.path.exists(poserdir)

    def get_default_poser_dir(self):
        appdir = self.config.appdir(require=False)
        if not appdir:
            appdir = os.path.join(sys.prefix, 'app')
        return os.path.join(appdir, 'poser')

    def make_poser_dir(self, path=None, **kwargs):
        """
        Create the directory structure for Poser.
        """
        # assume default path if none specified
        if not path:
            path = self.get_default_poser_dir()

        # path must not yet exist
        path = os.path.abspath(path)
        if os.path.exists(path):
            raise RuntimeError("folder already exists: {}".format(path))

        # make top-level dir
        os.makedirs(path)

        # normal refresh takes care of most of it
        self.refresh_poser_dir(path)

        # make git repo
        subprocess.check_call(['git', 'init', path])
        subprocess.check_call([
            'bash', '-c',
            "cd {} && git add poser .gitignore".format(path),
        ])

        return path

    def refresh_poser_dir(self, path=None, **kwargs):
        """
        Refresh the basic structure for Poser.
        """
        # assume default path if none specified
        if not path:
            path = self.get_default_poser_dir()

        # path must already exist
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise RuntimeError("folder does not exist: {}".format(path))

        # make poser pkg dir
        poser = os.path.join(path, 'poser')
        if not os.path.exists(poser):
            os.makedirs(poser)

        # add `__init__` stub
        init = os.path.join(poser, '__init__.py')
        if not os.path.exists(init):
            with open(init, 'wt') as f:
                pass

        # make 'db' subpackage
        db = os.path.join(poser, 'db')
        if not os.path.exists(db):
            os.makedirs(db)

        # add `__init__` stub
        init = os.path.join(db, '__init__.py')
        if not os.path.exists(init):
            with open(init, 'wt') as f:
                pass

        # make 'db.model' subpackage
        model = os.path.join(db, 'model')
        if not os.path.exists(model):
            os.makedirs(model)

        # add `__init__` stub
        init = os.path.join(model, '__init__.py')
        if not os.path.exists(init):
            with open(init, 'wt') as f:
                pass

        # make 'db:alembic' folder
        alembic = os.path.join(db, 'alembic')
        if not os.path.exists(alembic):
            os.makedirs(alembic)

        # make 'reports' subpackage
        reports = os.path.join(poser, 'reports')
        if not os.path.exists(reports):
            os.makedirs(reports)
        init = os.path.join(reports, '__init__.py')
        if not os.path.exists(init):
            with open(init, 'wt') as f:
                pass

        # make 'web' subpackage
        web = os.path.join(poser, 'web')
        if not os.path.exists(web):
            os.makedirs(web)
        init = os.path.join(web, '__init__.py')
        if not os.path.exists(init):
            with open(init, 'wt') as f:
                pass

        # make 'web.views' subpackage
        views = os.path.join(poser, 'web', 'views')
        if not os.path.exists(views):
            os.makedirs(views)
        init = os.path.join(views, '__init__.py')
        if not os.path.exists(init):
            with open(init, 'wt') as f:
                pass

        # make .gitignore
        gitignore = os.path.join(path, '.gitignore')
        # TODO: this should always overwrite a "managed" section of the file
        if not os.path.exists(gitignore):
            with open(gitignore, 'wt') as f:
                f.write('**/__pycache__/\n')

    def get_supported_report_flavors(self, **kwargs):
        # TODO: these should come from entry points etc.
        flavors = {
            'customer_py': {
                'description': "Query the Customer table (Python)",
                'template': '/reports/customer_py.mako',
                'output_fields': ['customer_number', 'customer_name'],
            },
            'customer_sql': {
                'description': "Query the Customer table (SQL)",
                'template': '/reports/customer_sql.mako',
                'output_fields': ['customer_number', 'customer_name'],
            },
            'product_py': {
                'description': "Query the Product table (Python)",
                'template': '/reports/product_py.mako',
                'output_fields': ['product_upc', 'product_description'],
            },
            'product_sql': {
                'description': "Query the Product table (SQL)",
                'template': '/reports/product_sql.mako',
                'output_fields': ['product_upc', 'product_description'],
            },
        }

        items = sorted(flavors.items(),
                       key=lambda itm: itm[1]['description'])

        items.insert(0, ('default', {
            'description': "Default (empty)",
            'template': '/reports/base.mako',
            'output_fields': [],
        }))

        return OrderedDict(items)

    def get_all_reports(self, ignore_errors=True, **kwargs):
        try:
            from poser import reports
        except:
            if ignore_errors:
                log.warning("cannot import poser reports module!")
                return []
            raise

        all_reports = []

        path = os.path.dirname(reports.__file__)
        for fname in os.listdir(path):
            if fname.startswith('_'):
                continue
            if not fname.endswith('.py'):
                continue

            key, ext = os.path.splitext(
                os.path.basename(fname))

            report = self.normalize_report(key)
            if report:
                all_reports.append(report)

        return all_reports

    def normalize_report(self, key, **kwargs):
        """
        Load the report module for the given key, and normalize the
        report it contains.
        """
        from poser import reports

        filepath = os.path.join(os.path.dirname(reports.__file__),
                                '{}.py'.format(key))

        modpath = '.'.join((reports.__name__, key))

        try:
            mod = import_module_path(modpath)
            import_reload(mod)

        except Exception as error:
            log.warning("import failed for %s", modpath, exc_info=True)
            return {
                'report_key': key,
                'module_file_path': filepath,
                'error': simple_error(error),
                'report': None,
                'report_name': '??',
                'description': '??',
            }

        for name in dir(mod):
            if name.startswith('_'):
                continue

            obj = getattr(mod, name)
            if (isinstance(obj, type)
                and issubclass(obj, ExcelReport)
                and obj.type_key
                and obj.type_key.startswith('poser_')):

                return {
                    'report': obj,
                    'module_file_path': filepath,
                    'report_key': key,
                    'report_name': obj.name,
                    'description': obj.__doc__,
                }

    def normalize_report_path(self, path, **kwargs):
        """
        Normalize the report module for the given file path.
        """
        from poser import reports

        # is module in the poser reports package?
        dirname = os.path.dirname(path)
        if dirname != os.path.dirname(reports.__file__):
            return

        # does module have a "normal" name?
        fname = os.path.basename(path)
        if fname.startswith('_'):
            return
        if not fname.endswith('.py'):
            return

        # okay then normalize per usual
        key, ext = os.path.splitext(fname)
        return self.normalize_report(key)

    def make_report(self, key, name, description,
                    flavor=None, output_fields=[], include_comments=True,
                    **kwargs):
        """
        Generate a new Python module for a Poser Report.
        """
        from poser import reports

        # TODO: make templates dir configurable
        templates = [resource_path('rattail:templates/poser')]
        templates = TemplateLookup(directories=templates)

        output_fields = output_fields or []
        template = '/reports/base.mako'
        if flavor:
            flavors = self.get_supported_report_flavors()
            if flavor in flavors:
                template = flavors[flavor]['template']
                output_fields = flavors[flavor]['output_fields']

        template = templates.get_template(template)

        cap_name = ''.join([word.capitalize()
                            for word in key.split('_')])

        context = {
            'app_title': self.config.app_title(),
            'key': key,
            'name': name,
            'cap_name': cap_name,
            'description': description,
            'output_fields': output_fields,
            'include_comments': include_comments,
        }

        path = os.path.join(os.path.dirname(reports.__file__),
                            '{}.py'.format(key))

        with open(path, 'wt') as f:
            f.write(template.render(**context))

        return self.normalize_report(key)

    def replace_report(self, key, path, **kwargs):
        """
        Replace the report module from the given file path.
        """
        from poser import reports

        report = self.normalize_report(key)
        oldpath = report['module_file_path']
        newpath = os.path.join(os.path.dirname(reports.__file__),
                               os.path.basename(path))

        if newpath != oldpath and os.path.exists(newpath):
            raise RuntimeError("Report already exists; cannot overwrite: {}".format(newpath))

        if os.path.exists(oldpath):
            os.remove(oldpath)

        with open(path, 'rb') as fin:
            with open(newpath, 'wb') as fout:
                fout.write(fin.read())

        return self.normalize_report_path(newpath)

    def delete_report(self, key, **kwargs):
        from poser import reports

        path = os.path.join(os.path.dirname(reports.__file__),
                            '{}.py'.format(key))
        if os.path.exists(path):
            os.remove(path)

    def get_all_tailbone_views(self, **kwargs):
        from poser.web import views

        all_views = []

        path = os.path.dirname(views.__file__)
        for fname in os.listdir(path):
            if fname.startswith('_'):
                continue
            if not fname.endswith('.py'):
                continue

            key, ext = os.path.splitext(
                os.path.basename(fname))

            view = self.normalize_view(key)
            if view:
                all_views.append(view)

        return all_views

    def normalize_tailbone_view(self, key, **kwargs):
        """
        Load the view module for the given key, and normalize the view
        it contains.
        """
        from tailbone.views import MasterView
        from poser.web import views

        filepath = os.path.join(os.path.dirname(views.__file__),
                                '{}.py'.format(key))

        modpath = '.'.join((views.__name__, key))

        try:
            mod = import_module_path(modpath)
            import_reload(mod)

        except Exception as error:
            log.warning("import failed for %s", modpath, exc_info=True)
            return {
                'key': key,
                'module_file_path': filepath,
                'error': simple_error(error),
                'view': None,
                'class_name': '??',
                'description': '??',
            }

        for name in dir(mod):
            if name.startswith('_'):
                continue

            obj = getattr(mod, name)
            if (isinstance(obj, type)
                and issubclass(obj, MasterView)
                and hasattr(obj, 'route_prefix')
                and obj.route_prefix.startswith('poser.')):

                return {
                    'key': key,
                    'module_file_path': filepath,
                    'view': obj,
                    'class_name': obj.__name__,
                    'description': obj.__doc__,
                }
