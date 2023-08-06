## -*- coding: utf-8; mode: python; -*-
<%inherit file="/reports/base.mako" />

<%def name="render_make_data_body()">\

        % if include_comments:
        # nb. your SQL query can return more columns than is needed
        # for output; any extras will be ignored.
        % endif

        <%text>##############################</%text>
        # example 1

        # looking for all customers
        sql = """
        select
                c.uuid as customer_uuid,
                c.number as customer_number,
                c.name as customer_name
        from
                customer c
        order by
                c.name
        """

        <%text>##############################</%text>
        # example 2

        # # all customers, joined with personal contact info
        # sql = """
        # select
        #         c.uuid as customer_uuid,
        #         c.number as customer_number,
        #         p.uuid as person_uuid,
        #         p.first_name,
        #         p.last_name,
        #         e.address as email_address
        # from
        #         customer c
        #         left outer join customer_x_person cp on cp.customer_uuid = c.uuid and cp.ordinal = 1
        #         left outer join person p on p.uuid = cp.person_uuid
        #         left outer join email e on e.parent_type = 'Person' and e.parent_uuid = p.uuid and e.ordinal = 1
        # order by
        #         c.name
        # """

        % if include_comments:
        # no need to process results, just return "as-is"...
        # nb. this approach only works if your SQL return column names
        # match/contain *at least* all of your report output columns.
        # but sequence of the result columns does not matter.
        % endif
        result = session.execute(sql)
        return list(result)
</%def>

${parent.body()}
