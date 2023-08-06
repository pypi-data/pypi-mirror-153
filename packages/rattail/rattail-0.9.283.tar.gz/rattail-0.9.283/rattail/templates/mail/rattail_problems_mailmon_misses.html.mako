## -*- coding: utf-8; -*-
<%inherit file="/base_problems.html.mako" />

<%def name="summary()">
  <p>
    There are ${len(problems)} Mailmon profiles which appear to have a
    "miss" problem - meaning, Mailmon may not be correctly identifying
    and processing new mail that comes in!&nbsp; Please investigate at
    your convenience.
  </p>
</%def>

<%def name="simple_row(obj, i)">
  <% account, profile, count = obj %>
  <tr>
    <td>${account.server}</td>
    <td>${profile.imap_folder}</td>
    <td>${count}</td>
  </tr>
</%def>

${self.simple_table(["IMAP Server", "IMAP Folder", "Messages"])}
