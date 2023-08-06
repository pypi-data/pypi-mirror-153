## -*- coding: utf-8; mode: python; -*-
<%inherit file="/reports/base.mako" />

<%def name="render_make_data_body()">\

        % if include_comments:
        # nb. your SQL query can return more columns than is needed
        # for output; any extras will be ignored.
        % endif

        <%text>##############################</%text>
        # example 1

        # looking for all products
        sql = """
        select
                p.uuid as product_uuid,
                p.upc as product_upc,
                p.description as product_description
        from
                product p
        order by
                p.description
        """

        <%text>##############################</%text>
        # example 2

        # # all products, joined with brand and reg. price
        # sql = """
        # select
        #         p.uuid as product_uuid,
        #         p.upc as product_upc,
        #         p.description as product_description,
        #         b.name as brand_name,
        #         rp.price as regular_price
        # from
        #         product p
        #         left outer join brand b on b.uuid = p.brand_uuid
        #         left outer join product_price rp on rp.uuid = p.regular_price_uuid
        # order by
        #         p.description
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
