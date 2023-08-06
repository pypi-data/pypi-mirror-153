## -*- coding: utf-8; -*-
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
    <h2>DataSync consumer for '${watcher.key}' -> '${consumer.key}' failed to process changes</h2>

    <p class="bold red">
      This consumer will <em>NOT</em> attempt to process any more changes until DataSync is restarted.
    </p>

    % if datasync_url is not Undefined and datasync_url:
        <a href="${datasync_url}">${datasync_url}</a>
    % endif

    <p>
      The '${consumer.key}' consumer made ${attempts} attempts to process new
      changes (with ${consumer.retry_delay} seconds between attempts), each of
      which resulted in the following error:
    </p>

    <pre class="indent">${error.__class__.__name__}: ${error}</pre>

    <p>
      The '${consumer.key}' consumer is normally set to process new changes
      from '${watcher.key}' every ${consumer.delay} seconds.&nbsp; (But
      again, DataSync must be restarted for this to resume.)
    </p>

    <p>Here is the full traceback for the exception:</p>

    <pre class="indent">${traceback}</pre>

  </body>
</html>
