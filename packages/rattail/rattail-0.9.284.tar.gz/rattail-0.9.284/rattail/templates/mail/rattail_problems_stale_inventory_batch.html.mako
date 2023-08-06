## -*- coding: utf-8; -*-
<%inherit file="/base_problems.html.mako" />

<%def name="summary()">
  <p>
    There are ${len(problems)} inventory batches which are considered
    stale.&nbsp; They were created at least ${cutoff_days} days ago and
    have yet to be executed.&nbsp; Please investigate at your
    convenience.
  </p>
</%def>

<%def name="simple_row(batch, i)">
  <tr>
    <td>${batch.id_str}</td>
    <td>${batch.description or ""}</td>
    <td>${render_time(batch.created)}</td>
    <td>${batch.created_by}</td>
    <td>${batch.rowcount}</td>
  </tr>
</%def>

${self.simple_table(["Batch ID", "Description", "Created", "Created by", "Rows"])}
