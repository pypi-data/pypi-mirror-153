## -*- coding: utf-8; -*-
<html>
  <body>
    <h2>${self.report_title()}</h2>

    ${self.summary()}

    ${self.render_params()}

    ${self.body()}
  </body>
</html>

## <%def name="report_title()">${output.report_name}</%def>
<%def name="report_title()">${report.name}</%def>

<%def name="summary()">
  <p>${report.__doc__}</p>
</%def>

<%def name="render_params()">
  <h3>Parameters</h3>
  <table border="1">
    % for key, value in params.items():
        <tr>
          <td>${key}</td>
          <td>${value}</td>
        </tr>
    % endfor
  </table>
</%def>
