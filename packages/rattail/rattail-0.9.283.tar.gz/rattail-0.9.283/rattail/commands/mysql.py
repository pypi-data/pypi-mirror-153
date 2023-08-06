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
MySQL-related commands
"""

from __future__ import unicode_literals, absolute_import

import sys

from rattail.commands import Subcommand


class MysqlChars(Subcommand):
    """
    View or update character set / collation info for a MySQL DB
    """
    name = 'mysql-chars'
    description = __doc__.strip()

    def add_parser_args(self, parser):

        parser.add_argument('--dbtype', metavar='TYPE', default='rattail.db',
                            help="Type of DB to inspect.  This must correspond to "
                            "a config section; the default is 'rattail.db'")
        parser.add_argument('--dbkey', metavar='KEY', default='default',
                            help="Config key for DB to inspect.  This must "
                            "correspond to one of the keys within the config "
                            "section identified by --dbtype; the default key is "
                            "'default'")
        parser.add_argument('--dburl', metavar='URL',
                            help="Explicit URL for DB to inspect.  If possible "
                            "you should use --dbtype and --dbkey instead.  If you "
                            "do use --dburl, this value must be in the format "
                            "supported by SQLAlchemy.")

        parser.add_argument('--charset',
                            help="Desired character set for the DB.")
        parser.add_argument('--collation',
                            help="Desired collation for the DB.")

        parser.add_argument('--table',
                            help="Show column info for the specified table.")
        parser.add_argument('--all-tables', action='store_true',
                            help="Show column info for all tables in the DB.")

        parser.add_argument('--offenders', action='store_true',
                            help="Show only \"offenders\" which do not match "
                            "the desired charset and/or collation.  If this is "
                            "not specified, all info will be shown for the "
                            "object(s) regardless of their charset/collation.")

        parser.add_argument('--fix', action='store_true',
                            help="Execute SQL to convert charset and/or collation "
                            "for relevant objects.  Note, this will affect \"all\" "
                            "objects in scope unless --offenders is specified, in "
                            "which case only those are affected.")
        parser.add_argument('--dry-run', action='store_true',
                            help="Emit the SQL statements to fix/convert entities "
                            "to STDOUT instead of executing the SQL directly.  Note "
                            "that this is only used if --fix is specified.")

    def run(self, args):
        import sqlalchemy as sa
        from rattail.db.config import get_engines

        if args.dburl:
            engine = sa.create_engine(args.dburl)

        else:
            engines = get_engines(self.config, args.dbtype)
            if not engines:
                self.stderr.write("No DB engines found for type: {}\n".format(
                    args.dbtype))
                sys.exit(1)
            if args.dbkey not in engines:
                self.stderr.write("DB key {} not found for type: {}\n".format(
                    args.dbkey, args.dbtype))
                sys.exit(1)
            engine = engines[args.dbkey]

        if engine.dialect.name != 'mysql':
            self.stderr.write("dialect '{}' not supported: {}\n".format(
                engine.dialect.name, engine))
            sys.exit(1)

        if args.fix:
            self.fix_db(engine, args)
        else:
            self.view_db(engine, args)

    def view_db(self, engine, args):
        import sqlalchemy as sa

        self.stdout.write("\n  {}\n".format(repr(engine.url)))
        self.stdout.write("\n  desired charset:   {}\n".format(args.charset))
        self.stdout.write("  desired collation: {}\n".format(args.collation))
        self.stdout.write("\n  showing db info:  {}\n".format(
            'offenders' if args.offenders else 'all'))
        tables = ['(none)']
        if args.all_tables:
            tables = ['(all)']
        elif args.table:
            tables = [args.table]
        self.stdout.write("  showing table(s): {}\n\n".format(','.join(tables)))

        dbinfo = self.fetch_dbinfo(engine, args)
        if dbinfo:
            self.show_results(dbinfo)
            self.stdout.write("\n")

        tablesinfo = self.fetch_tablesinfo(engine, args,
                                           offenders_only=args.offenders)
        if tablesinfo:
            self.show_results(tablesinfo)
            self.stdout.write("\n")

        tables = []
        if args.all_tables:
            tables = [info.TABLE_NAME for info in self.fetch_tablesinfo(
                engine, args, offenders_only=False)]
        elif args.table:
            tables = [args.table]
        for table in tables:
            colsinfo = self.fetch_colsinfo(engine, args, table)
            if colsinfo:
                self.stdout.write("  Table: {}\n\n".format(table))
                self.show_results(colsinfo)
                self.stdout.write("\n")

    def fix_db(self, engine, args):
        import sqlalchemy as sa

        if args.dry_run:
            self.stdout.write("\n")

        dbinfo = self.fetch_dbinfo(engine, args)
        if dbinfo:

            sql = """
            ALTER DATABASE :dbname CHARACTER SET :charset COLLATE :collation;
            """.strip()
            stmt = sa.text(sql).bindparams(dbname=engine.url.database,
                                           charset=args.charset,
                                           collation=args.collation)

            if args.dry_run:
                self.stdout.write("-- fix database\n")
                self.stdout.write("{}\n".format(stmt.compile(
                    dialect=engine.dialect,
                    compile_kwargs={'literal_binds': True})))
                self.stdout.write("\n")

            else:
                raise NotImplementedError

        tablesinfo = self.fetch_tablesinfo(engine, args,
                                           offenders_only=args.offenders)
        if tablesinfo:
            if args.dry_run:
                self.stdout.write("-- fix tables\n")

            sql = """
            ALTER TABLE :table CONVERT TO CHARACTER SET :charset COLLATE :collation;
            """.strip()

            for tableinfo in tablesinfo:
                stmt = sa.text(sql).bindparams(table=tableinfo.TABLE_NAME,
                                               charset=args.charset,
                                               collation=args.collation)

                if args.dry_run:
                    self.stdout.write("{}\n".format(stmt.compile(
                        dialect=engine.dialect,
                        compile_kwargs={'literal_binds': True})))

                else:
                    raise NotImplementedError

            if args.dry_run:
                self.stdout.write("\n")

        tables = []
        if args.all_tables:
            tables = [info.TABLE_NAME for info in self.fetch_tablesinfo(
                engine, args, offenders_only=False)]
        elif args.table:
            tables = [args.table]
        unknown_data_types = set()
        for table in tables:
            colsinfo = self.fetch_colsinfo(engine, args, table)
            if colsinfo:
                if args.dry_run:
                    printed_header = False

                sql = """
                ALTER TABLE :table MODIFY :column {}({}) CHARACTER SET :charset COLLATE :collation;
                """.strip()

                for colinfo in colsinfo:
                    colsql = sql.format(colinfo.DATA_TYPE,
                                        colinfo.CHARACTER_MAXIMUM_LENGTH)
                    stmt = sa.text(colsql).bindparams(table=tableinfo.TABLE_NAME,
                                                      column=colinfo.COLUMN_NAME,
                                                      charset=args.charset,
                                                      collation=args.collation)

                    if args.dry_run:
                        if not printed_header:
                            self.stdout.write("-- fix columns for: {}\n".format(table))
                            printed_header = True
                        self.stdout.write("{}\n".format(stmt.compile(
                            dialect=engine.dialect,
                            compile_kwargs={'literal_binds': True})))

                    else:
                        raise NotImplementedError

                if args.dry_run and printed_header:
                    self.stdout.write("\n")

    def fetch_dbinfo(self, engine, args):
        import sqlalchemy as sa

        SCHEMATA = sa.sql.table(
            'SCHEMATA',
            sa.sql.column('SCHEMA_NAME'),
            sa.sql.column('DEFAULT_CHARACTER_SET_NAME'),
            sa.sql.column('DEFAULT_COLLATION_NAME'),
            schema='information_schema')

        query = sa.sql.select(columns=[SCHEMATA.c.SCHEMA_NAME,
                                       SCHEMATA.c.DEFAULT_CHARACTER_SET_NAME,
                                       SCHEMATA.c.DEFAULT_COLLATION_NAME])\
                      .where(SCHEMATA.c.SCHEMA_NAME == engine.url.database)\
                      .order_by(SCHEMATA.c.SCHEMA_NAME)

        if args.offenders:
            query = query.where(sa.or_(
                SCHEMATA.c.DEFAULT_CHARACTER_SET_NAME != args.charset,
                SCHEMATA.c.DEFAULT_COLLATION_NAME != args.collation))

        cursor = engine.execute(query)
        return cursor.fetchall()

    def fetch_tablesinfo(self, engine, args, offenders_only=False):
        import sqlalchemy as sa

        TABLES = sa.sql.table(
            'TABLES',
            sa.sql.column('TABLE_SCHEMA'),
            sa.sql.column('TABLE_NAME'),
            sa.sql.column('TABLE_TYPE'),
            sa.sql.column('TABLE_COLLATION'),
            schema='information_schema')

        query = sa.sql.select(columns=[TABLES.c.TABLE_NAME,
                                       TABLES.c.TABLE_COLLATION])\
                      .where(TABLES.c.TABLE_SCHEMA == engine.url.database)\
                      .where(TABLES.c.TABLE_TYPE.like('BASE_TABLE'))\
                      .order_by(TABLES.c.TABLE_NAME)

        if args.table:
            query = query.where(TABLES.c.TABLE_NAME == args.table)

        if offenders_only:
            query = query.where(TABLES.c.TABLE_COLLATION != args.collation)

        cursor = engine.execute(query)
        return cursor.fetchall()

    def fetch_colsinfo(self, engine, args, table):
        import sqlalchemy as sa

        COLUMNS = sa.sql.table(
            'COLUMNS',
            sa.sql.column('TABLE_SCHEMA'),
            sa.sql.column('TABLE_NAME'),
            sa.sql.column('COLUMN_NAME'),
            sa.sql.column('CHARACTER_SET_NAME'),
            sa.sql.column('COLLATION_NAME'),
            sa.sql.column('DATA_TYPE'),
            sa.sql.column('CHARACTER_MAXIMUM_LENGTH'),
            schema='information_schema')

        query = sa.sql.select(columns=[COLUMNS.c.COLUMN_NAME,
                                       COLUMNS.c.DATA_TYPE,
                                       COLUMNS.c.CHARACTER_MAXIMUM_LENGTH,
                                       COLUMNS.c.CHARACTER_SET_NAME,
                                       COLUMNS.c.COLLATION_NAME])\
                      .where(COLUMNS.c.TABLE_SCHEMA == engine.url.database)\
                      .where(COLUMNS.c.TABLE_NAME == table)\
                      .where(COLUMNS.c.DATA_TYPE == 'varchar')\
                      .order_by(COLUMNS.c.COLUMN_NAME)

        if args.offenders:
            query = query.where(sa.or_(
                COLUMNS.c.CHARACTER_SET_NAME != args.charset,
                COLUMNS.c.COLLATION_NAME != args.collation))

        cursor = engine.execute(query)
        return cursor.fetchall()

    def show_results(self, rows):
        import texttable

        table = texttable.Texttable()

        # add a header row, plus all data rows
        table.add_rows([rows[0].keys()] + rows)

        self.stdout.write("{}\n".format(table.draw()))
