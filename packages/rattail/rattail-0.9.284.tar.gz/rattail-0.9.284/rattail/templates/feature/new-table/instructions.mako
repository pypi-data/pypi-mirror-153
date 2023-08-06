## -*- mode: markdown; -*-
# New Table: ${prefixed_model_name}

Create a new Python module under `${app_package}.db.model`, for instance at
`~/src/${app_slug}/${app_package}/db/model/${table_name}.py`, with contents:

```python
"""
Table schema for ${model_title_plural}
"""

import sqlalchemy as sa
# from sqlalchemy import orm

from rattail.db.model import Base, uuid_column


class ${prefixed_model_name}(Base):
    """
    ${description}
    """
    __tablename__ = '${prefixed_table_name}'
    model_title = "${model_title}"
    model_title_plural = "${model_title_plural}"
    % if versioned:

    # this enables data versioning for the table
    __versioned__ = {}
    % endif

    # universally-unique identifier
    uuid = uuid_column()
    % for column in columns:

    ${column['name']} = sa.Column(sa.${column['data_type']}, nullable=${column['nullable']}, doc="""
    ${column['description']}
    """)
    % endfor

    # TODO: you usually should define the __str__() method

    # def __str__(self):
    #     return self.name or ""
```

You should review all code in the module, and edit as needed, before
continuing.

Make sure to bring it into your root model namespace also, for instance in
`~/src/${app_slug}/${app_package}/db/model/__init__.py` add this:

```python
from .${table_name} import ${prefixed_model_name}
```

Then generate a new Alembic version script for the schema migration:

```sh
cd ${envroot}
bin/alembic -c app/rattail.conf revision --autogenerate --head ${app_package}@head -m "add ${prefixed_table_name}"
```

That should create a new script somewhere in e.g.
`~/src/${app_slug}/${app_package}/db/alembic/versions/`.

Edit the migration script as needed, then apply it to your database:

```sh
cd ${envroot}
bin/alembic -c app/rattail.conf upgrade heads
```

At this point your DB should have the new table.  You can see details with:

```sh
sudo -u postgres psql -c '\d ${prefixed_table_name}' ${app_package}
```

Once you are happy with the result, don't forget to commit!

```sh
cd ~/src/${app_slug}
git add .
git commit -m "add model for ${prefixed_model_name}"
```

For more help please see the
[Rattail Manual](https://rattailproject.org/docs/rattail-manual/),
in particular these sections:

- [Rattail Database](https://rattailproject.org/docs/rattail-manual/data/db/index.html)
