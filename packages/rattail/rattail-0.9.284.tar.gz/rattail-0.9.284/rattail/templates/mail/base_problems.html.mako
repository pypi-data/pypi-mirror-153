## -*- coding: utf-8; -*-
<html>
  <head>
    <style type="text/css">
      a {
          text-decoration: none;
      }
      table {
          border-collapse: collapse;
          border-right: 1px solid gray;
          border-bottom: 1px solid gray;
      }
      th, td {
          border-left: 1px solid gray;
          border-top: 1px solid gray;
          padding: 3px 4px;
      }
    </style>
  </head>
  <body>
    <h2>${self.problem_title()}</h2>
    <h3>System:&nbsp; ${system_title}</h3>

    ${self.summary()}

    ${self.body()}
  </body>
</html>

<%def name="problem_title()">${report.problem_title}</%def>

<%def name="summary()">
  <p>There were ${len(problems)} problems found of this sort.</p>
  <p>Please investigate at your convenience.</p>
</%def>

<%def name="simple_table(columns)">
  <table>
    <thead>
      <tr>
        % for column in columns:
            <th>${column}</th>
        % endfor
     </tr>
    </thead>
    <tbody>
      % for i, obj in enumerate(problems):
          ${self.simple_row(obj, i)}
      % endfor
    </tbody>
  </table>
</%def>

<%def name="simple_row(obj, i)">
  <tr>
    <td>TODO: you must define this yourself</td>
  </tr>
</%def>
