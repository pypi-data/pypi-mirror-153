## -*- mode: markdown; -*-
# New Report: ${name}

Create a new Python module under `${app_package}.reports`, for instance at
`~/src/${app_slug}/${app_package}/reports/${code_name}.py`, with contents:

```python
"""
"${name}" report
"""

# from sqlalchemy import orm

from rattail.reporting import ExcelReport

from ${app_package}.db import model


class ${cap_name}(ExcelReport):
    """
    ${description}
    """
    type_key = '${app_prefix}_${code_name}'
    name = "${name}"

    # TODO: you must declare all desired output columns for Excel
    output_fields = [
        'customer_number',
        'customer_name',
    ]

    def make_data(self, session, params, progress=None, **kwargs):

        # TODO: obviously you must do whatever queries you need, to gather
        # all data required for your report

        # looking for all customers
        customers = session.query(model.Customer)\ 
                         .order_by(model.Customer.number) #\ 
                         # .options(orm.joinedload(model.Customer._people)\ 
                         #          .joinedload(model.CustomerPerson.person))

        # returned object will be a list of dicts
        rows = []

        def include(customer, i):
            # person = customer.only_person()
            rows.append({
                'customer_number': customer.number,
                'customer_name': customer.name,
            })

        self.progress_loop(include, customers, progress,
                           message="Fetching data for report")
        return rows
```

For more help please see the
[Rattail Manual](https://rattailproject.org/docs/rattail-manual/),
in particular these sections:

- [Reports](https://rattailproject.org/docs/rattail-manual/data/reports/index.html)
