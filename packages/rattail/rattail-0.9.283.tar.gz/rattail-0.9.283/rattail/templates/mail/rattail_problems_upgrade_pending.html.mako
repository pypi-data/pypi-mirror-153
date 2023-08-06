## -*- coding: utf-8; -*-
<%inherit file="/base_problems.html.mako" />

<%def name="summary()">
  <p>
    There are ${len(problems)} system upgrades which are currently pending.
  </p>
</%def>

<%def name="simple_row(upgrade, i)">
  <tr>
    <td>${upgrade.description}</td>
    <td>${render_time(upgrade.created)}</td>
    <td>${upgrade.created_by}</td>
    <td>${enum.UPGRADE_STATUS[upgrade.status_code]}</td>
  </tr>
</%def>

${self.simple_table(["Description", "Created", "Created by", "Status"])}
