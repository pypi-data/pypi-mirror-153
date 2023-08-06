## -*- coding: utf-8 -*-
<html>
  <head>
    <style type="text/css">
      .bold {
          font-weight: bold;
      }
      .red {
          color: red;
      }
      .indent {
          margin-left: 2em;
      }
    </style>
  </head>
  <body>
    <h2>DataSync '${watcher.key}' watcher failed to get changes</h2>

    <p class="bold red">
      This watcher will <em>NOT</em> look for new changes until DataSync is restarted.
    </p>

    % if datasync_url is not Undefined and datasync_url:
        <a href="${datasync_url}">${datasync_url}</a>
    % endif

    <p>
      The '${watcher.key}' watcher made ${attempts} attempts to look for new
      changes (with ${watcher.retry_delay} seconds between attempts), each of which
      resulted in the following error:
    </p>

    <pre class="indent">${error.__class__.__name__}: ${error}</pre>

    % if watcher.consumes_self:
        <p>
          The '${watcher.key}' watcher consumes its own changes, and has no
          other data consumers configured.
        </p>
    % else:
        <p>
          The '${watcher.key}' watcher is meant to provide changes to the following data consumers:
        </p>
        <ul>
          % for consumer in watcher.consumer_stub_keys:
              <li>${consumer}</li>
          % endfor
        </ul>
    % endif

    <p>
      The '${watcher.key}' watcher is normally set to look for new changes
      every ${watcher.delay} seconds.&nbsp; (But again, DataSync must be
      restarted for this to resume.)
    </p>

    <p>Here is the full traceback for the exception:</p>

    <pre class="indent">${traceback}</pre>

  </body>
</html>
