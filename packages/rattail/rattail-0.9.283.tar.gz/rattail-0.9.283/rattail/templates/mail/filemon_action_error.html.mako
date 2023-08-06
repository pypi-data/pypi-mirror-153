## -*- coding: utf-8 -*-
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
          text-align: left;
      }
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
    <h2>Error invoking FileMon action</h2>

    <p class="bold red">
      FileMon will <em>NOT</em> attempt to invoke any further actions on this
      file until it is restarted.
    </p>

    <p>
      While attempting to invoke some action(s) on a file, FileMon encountered
      an error; here are the details:
    </p>

    <table>
      <tbody>
        <tr>
          <th>Host Name</th>
          <td>${hostname}</td>
        </tr>
        <tr>
          <th>File Path</th>
          <td>${path}</td>
        </tr>
        <tr>
          <th>Action Spec</th>
          <td>${action.spec}</td>
        </tr>
        <tr>
          <th>Attempts Made</th>
          <td>${attempts}</td>
        </tr>
        % if attempts > 1:
            <tr>
              <th>Attempt Delay</th>
              <td>${action.retry_delay} seconds</td>
            </tr>
        % endif
        <tr>
          <th>Error Type</th>
          <td>${error.__class__.__name__}</td>
        </tr>
        <tr>
          <th>Error Text</th>
          <td>${error}</td>
        </tr>
      </tbody>
    </table>

    <p>Here is the full traceback for the exception:</p>

    <pre class="indent">${traceback}</pre>

  </body>
</html>
