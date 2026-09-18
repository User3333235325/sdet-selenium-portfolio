"""A small local HTML form app, so the form test owns its own environment.

The test used to drive a public practice page. That page is fine to explore by
hand, but it serves ads: frames load late, the layout shifts under the test, and
a banner can end up over the submit button. None of that is a defect in the
application under test, so none of it belongs in a test result.

This module serves an equivalent form from localhost for the duration of the
session. The test still does real work - real navigation, a real form POST, a
real response page - it just stops depending on a third party to stay still.
"""

from __future__ import annotations

import threading
from contextlib import contextmanager
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Iterator, List, Tuple
from urllib.parse import parse_qsl

FORM_PATH = "/"
SUBMIT_PATH = "/submitted"

FORM_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>HTML Form</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 2rem; max-width: 40rem; }
    label { display: block; margin-top: 1rem; font-weight: 600; }
    input[type="text"], input[type="password"], textarea, select { width: 100%; }
    input[type="submit"] { margin-top: 1.5rem; padding: 0.5rem 1.5rem; }
  </style>
</head>
<body>
  <h1>HTML Form</h1>
  <form id="html-form" action="/submitted" method="post">
    <label for="username">Username</label>
    <input type="text" id="username" name="username">

    <label for="password">Password</label>
    <input type="password" id="password" name="password">

    <label for="comments">Comments</label>
    <textarea id="comments" name="comments" rows="4"></textarea>

    <label for="filename">File name</label>
    <input type="text" id="filename" name="filename" value="notes.txt">

    <label for="dropdown">Dropdown</label>
    <select id="dropdown" name="dropdown">
      <option value="dd1">Drop Down Item 1</option>
      <option value="dd2">Drop Down Item 2</option>
    </select>

    <label><input type="checkbox" id="checkbox1" name="checkboxes" value="cb1"> Checkbox 1</label>

    <input type="submit" name="submitbutton" value="submit">
    <input type="reset" name="resetbutton" value="reset">
  </form>
</body>
</html>
"""

NOT_FOUND_HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Not Found</title></head>
<body><h1>Not Found</h1></body></html>
"""


def results_html(fields: List[Tuple[str, str]]) -> str:
    """Render the response page that the form POSTs to."""
    rows = "\n".join(
        f"      <tr><td>{escape(name)}</td><td>{escape(value)}</td></tr>"
        for name, value in fields
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Processed Form Details</title></head>
<body>
  <h1>Processed Form Details</h1>
  <p id="submission-message">You submitted the form.</p>
  <table id="submitted-values">
    <tbody>
      <tr><th>Field</th><th>Value</th></tr>
{rows}
    </tbody>
  </table>
</body>
</html>
"""


class FormRequestHandler(BaseHTTPRequestHandler):
    """Serves the form on GET and echoes the submitted values on POST."""

    protocol_version = "HTTP/1.1"

    def do_GET(self) -> None:  # noqa: N802 - name fixed by BaseHTTPRequestHandler
        if self.path.split("?", 1)[0] != FORM_PATH:
            self._respond(404, NOT_FOUND_HTML)
            return
        self._respond(200, FORM_HTML)

    def do_POST(self) -> None:  # noqa: N802 - name fixed by BaseHTTPRequestHandler
        if self.path != SUBMIT_PATH:
            self._respond(404, NOT_FOUND_HTML)
            return
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        self._respond(200, results_html(parse_qsl(body, keep_blank_values=True)))

    def _respond(self, status: int, body: str) -> None:
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args: object) -> None:
        """Stay quiet so pytest output only carries test results."""


@contextmanager
def serve_form(host: str = "127.0.0.1") -> Iterator[str]:
    """Run the form app on an ephemeral port and yield its base URL."""
    server = ThreadingHTTPServer((host, 0), FormRequestHandler)
    server.daemon_threads = True
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://{host}:{server.server_address[1]}/"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
