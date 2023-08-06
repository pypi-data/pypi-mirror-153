## -*- coding: utf-8; mode: python; -*-
<%inherit file="/reports/base.mako" />

<%def name="render_make_data_body()">\
        model = self.model

        <%text>##############################</%text>
        # example 1

        # looking for all customers
        customers = session.query(model.Customer)<%text>\</%text>
                           .order_by(model.Customer.name)

        <%text>##############################</%text>
        # example 2

        # # all customers, joined with personal contact info
        # from sqlalchemy import orm
        # customers = session.query(model.Customer)<%text>\</%text>
        #                    .order_by(model.Customer.number)<%text>\</%text>
        #                    .options(orm.joinedload(model.Customer._people)<%text>\</%text>
        #                                .joinedload(model.CustomerPerson.person)<%text>\</%text>
        #                                .joinedload(model.Person.emails))

        # final return object will be a list of dicts
        results = []

        % if include_comments:
        # nb. the next include() function + progress_loop() is really
        # just a glorified "for each" loop, but allows the web app to
        # show progress
        % endif

        def include(customer, i):

            % if include_comments:
            # nb. must assign values for all of the report output
            # columns; extra non-output values will be ignored
            % endif
            result = {
                'customer_number': customer.number,
                'customer_name': customer.name,
            }

            # # example 2
            # person = customer.first_person()
            # result.update{
            #     'first_name': person.first_name if person else None,
            #     'last_name': person.first_name if person else None,
            #     'email_address': person.first_email_address() if person else None,
            # })

            results.append(result)

        self.progress_loop(include, customers, progress,
                           message="Fetching data for report")
        return results
</%def>

${parent.body()}
