## -*- coding: utf-8; -*-
<html>
  <head>
    <style type="text/css">
      label {
          font-weight: bold;
      }
    </style>
  </head>
  <body>
    <h1>Command Result</h1>

    <label>Command</label>
    <p><code>${cmd}</code></p>

    <label>Runtime</label>
    <p>${runtime} (${runtime_pretty})</p>

    <label>Exit Code</label>
    <p>${retcode}</p>

    <label>Output</label>
    <pre>${output}</pre>

  </body>
</html>
