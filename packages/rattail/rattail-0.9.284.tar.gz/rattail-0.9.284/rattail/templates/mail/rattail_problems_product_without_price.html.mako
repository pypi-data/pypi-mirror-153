## -*- coding: utf-8; -*-
<%inherit file="/base_problems.html.mako" />

<%def name="summary()">
  <p>
    There are ${len(problems)} products which have "empty" (null or $0) price.
  </p>
</%def>

<%def name="simple_row(product, i)">
  <tr>
    <td>${product.upc.pretty() if product.upc else ""}</td>
    <td>${product.brand or ""}</td>
    <td>${product.description}</td>
    <td>${product.department or ""}</td>
    <td>
      % if product.regular_price and product.regular_price.price is not None:
          $ ${product.regular_price.price}
      % endif
    </td>
  </tr>
</%def>

${self.simple_table(["UPC", "Brand", "Description", "Department", "Price"])}
