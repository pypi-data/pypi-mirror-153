## -*- coding: utf-8 -*-
<html>
  <head>
    <style type="text/css">

      table {
          border-collapse: collapse;
          border-left: 1px solid black;
          border-top: 1px solid black;
          font-size: 11pt;
          margin-left: 50px;
          min-width: 80%;
      }

      table th,
      table td {
          border-bottom: 1px solid black;
          border-right: 1px solid black;
      }

      table td {
          padding: 5px 10px;
      }

      table td.value {
          font-family: monospace;
          white-space: pre;
      }

      table.new td.host-value,
      table.diff tr.diff td.host-value {
          background-color: #cfc;
      }

      table.deleted td.local-value,
      table.diff tr.diff td.local-value {
          background-color: #fcc;
      }

    </style>
  </head>
  <body>
    <h3>Warnings for ${host_title} -> ${local_title} data ${direction}</h3>
    % if dry_run:
        <p>
          <em><strong>NOTE:</strong>&nbsp; This was a dry run only; no data was harmed
          in the making of this email.</em>
        </p>
    % endif
    <p>
      Generally this periodic data import is expected to be a precaution only,
      in order to detect and fix ${local_title} data which has fallen out of sync
      from ${host_title}.&nbsp; It is normally intended that proper real-time
      operation (e.g. a 'datasync' daemon) <em>should</em> be enough to keep things
      in sync; therefore any net changes which occur as a result of this periodic
      import process are considered warnings.
    </p>
      The following is a list of changes which occurred during the latest import run.&nbsp;
      % if not dry_run:
          (Note that this was not a dry run; these changes have been committed
          to the ${local_title} system.)&nbsp;
      % endif
      Please investigate at your convenience.
    </p>
    <ul>
      % for model, (created, updated, deleted) in changes.items():
          <li>
            <a href="#${model}">${model}</a>
            - ${'{:,d}'.format(len(created))} created, ${'{:,d}'.format(len(updated))} updated, ${'{:,d}'.format(len(deleted))} deleted
          </li>
      % endfor
    </ul>
    <p>
      Here is the full import command, which took ${runtime} to run:
    </p>
    <p style="padding-left: 20px;">
      <code>${argv}</code>
    <p>
    % for model, (created, updated, deleted) in changes.items():
        <h4>
          <a name="${model}">${model}</a>
          - ${'{:,d}'.format(len(created))} created, ${'{:,d}'.format(len(updated))} updated, ${'{:,d}'.format(len(deleted))} deleted
        </h4>

        % for instance, host_data in created[:max_display]:
            <h5>${model} - ${render_record(instance)} was <em>created</em> in ${local_title}:</h5>
            <table class="new">
              <thead>
                <tr>
                  <th>field name</th>
                  <th>old value</th>
                  <th>new value</th>
                </tr>
              </thead>
              <tbody>
                % for field in sorted(host_data):
                   <tr>
                     <td class="field">${field}</td>
                     <td class="value local-value">&nbsp;</td>
                     <td class="value host-value">${repr(host_data[field])}</td>
                   </tr>
                % endfor
              </tbody>
            </table>
        % endfor
        % if len(created) > max_display:
            <h5>${model} - there were ${'{:,d}'.format(len(created) - max_display)} other additions which are not shown here</h5>
        % endif

        % for instance, local_data, host_data in updated[:max_display]:
            <h5>${model} - ${render_record(instance)} was <em>updated</em> in ${local_title}:</h5>
            <table class="diff">
              <thead>
                <tr>
                  <th>field name</th>
                  <th>old value</th>
                  <th>new value</th>
                </tr>
              </thead>
              <tbody>
                % for field in sorted(local_data):
                   % if field in host_data:
                       <tr${' class="diff"' if local_data[field] != host_data[field] else ''|n}>
                         <td class="field">${field}</td>
                         <td class="value local-value">${repr(local_data[field])}</td>
                         <td class="value host-value">${repr(host_data[field])}</td>
                       </tr>
                    % endif
                % endfor
              </tbody>
            </table>
        % endfor
        % if len(updated) > max_display:
            <h5>${model} - there were ${'{:,d}'.format(len(updated) - max_display)} other updates which are not shown here</h5>
        % endif

        % for instance, local_data in deleted[:max_display]:
            <h5>${model} - ${render_record(instance)} was <em>deleted</em> from ${local_title}:</h5>
            <table class="deleted">
              <thead>
                <tr>
                  <th>field name</th>
                  <th>old value</th>
                  <th>new value</th>
                </tr>
              </thead>
              <tbody>
                % for field in sorted(local_data):
                   <tr>
                     <td class="field">${field}</td>
                     <td class="value local-value">${repr(local_data[field])}</td>
                     <td class="value host-value">&nbsp;</td>
                   </tr>
                % endfor
              </tbody>
            </table>
        % endfor
        % if len(deleted) > max_display:
            <h5>${model} - there were ${'{:,d}'.format(len(deleted) - max_display)} other deletions which are not shown here</h5>
        % endif

    % endfor
  </body>
</html>
