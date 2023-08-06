## -*- coding: utf-8; mode: python; -*-
<%inherit file="/reports/base.mako" />

<%def name="render_make_data_body()">\
        model = self.model

        <%text>##############################</%text>
        # example 1

        # looking for all products
        products = session.query(model.Product)<%text>\</%text>
                          .order_by(model.Product.description)

        <%text>##############################</%text>
        # example 2

        # # all products, joined with brand and reg. price
        # from sqlalchemy import orm
        # products = session.query(model.Product)<%text>\</%text>
        #                   .outerjoin(model.Brand)\
        #                   .order_by(model.Brand.name,
        #                             model.Product.description)<%text>\</%text>
        #                   .options(orm.joinedload(model.Product.brand))<%text>\</%text>
        #                   .options(orm.joinedload(model.Product.regular_price))

        # final return object will be a list of dicts
        results = []

        % if include_comments:
        # nb. the next include() function + progress_loop() is really
        # just a glorified "for each" loop, but allows the web app to
        # show progress
        % endif

        def include(product, i):

            % if include_comments:
            # nb. must assign values for all of the report output
            # columns; extra non-output values will be ignored
            % endif
            result = {
                'product_upc': str(product.upc or ''),
                'product_description': product.description,
            }

            # # example 2
            # brand = product.brand
            # regprice = product.regular_price
            # result.update{
            #     'brand_name': brand.name if brand else None,
            #     'regular_price': regprice.price if regprice else None,
            # })

            results.append(result)

        self.progress_loop(include, products, progress,
                           message="Fetching data for report")
        return results
</%def>

${parent.body()}
