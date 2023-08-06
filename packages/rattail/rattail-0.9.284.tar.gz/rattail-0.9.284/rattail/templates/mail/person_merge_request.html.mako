## -*- coding: utf-8; -*-
<html>
  <body>
    <h2>Request to Merge 2 People</h2>

    <p>
      A request to merge the following 2 people was submitted by ${user_display}.
    </p>

    <ul>
      <li>
        % if removing_url is not Undefined and removing_url:
            <a href="${removing_url}">${removing_display}</a>
        % else:
            ${removing_display}
        % endif
      </li>
      <li>
        % if keeping_url is not Undefined and keeping_url:
            <a href="${keeping_url}">${keeping_display}</a>
        % else:
            ${keeping_display}
        % endif
      </li>
    </ul>

    % if merge_request_url is not Undefined and merge_request_url:
        <p><a href="${merge_request_url}">View this Merge Request</a></p>
    % endif

  </body>
</html>
