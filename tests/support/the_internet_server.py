"""A small local stand-in for the-internet's login flow.

the-internet.herokuapp.com is a well-known practice site, but it is personal,
free-tier infrastructure with no uptime guarantee. It has twice caused this
suite to fail from a wholly unresponsive renderer, not from anything wrong in
our own code. This serves an equivalent login flow from localhost, so the
smoke suite does not depend on that site staying up to pass.

Only the login flow is reproduced: GET /login, POST /authenticate, and the
resulting /secure page, using the same ids and structure the real site uses
(#username, #password, #flash, .example h2) so the page objects are
unchanged. The real site carries its one-time flash message in a server-side
session; this stand-in carries it in a query parameter on the post-login
redirect instead - simpler, and indistinguishable from the browser's side.
"""

from __future__ import annotations

import threading
from contextlib import contextmanager
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Iterator, Optional
from urllib.parse import parse_qsl, quote, urlparse

VALID_USERNAME = "tomsmith"
VALID_PASSWORD = "SuperSecretPassword!"

LOGIN_PATH = "/login"
AUTH_PATH = "/authenticate"
SECURE_PATH = "/secure"

NOT_FOUND_HTML = "<!DOCTYPE html><html><body><h1>Not Found</h1></body></html>"


def _page(heading: str, flash: Optional[str], body: str) -> str:
    flash_html = f'<div id="flash" class="flash">{escape(flash)}</div>' if flash else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>{escape(heading)}</title></head>
<body>
{flash_html}
<div class="example">
  <h2>{escape(heading)}</h2>
  {body}
</div>
</body>
</html>
"""


def _login_page(flash: Optional[str]) -> str:
    form = """
    <form name="login" method="post" action="/authenticate">
      <div class="row"><label for="username">Username</label>
        <input type="text" id="username" name="username"></div>
      <div class="row"><label for="password">Password</label>
        <input type="password" id="password" name="password"></div>
      <button type="submit" class="radius">Login</button>
    </form>
    """
    return _page("Login Page", flash, form)


def _secure_page(flash: Optional[str]) -> str:
    body = '<a href="/logout" class="button secondary radius">Logout</a>'
    return _page("Secure Area", flash, body)


class LoginFlowHandler(BaseHTTPRequestHandler):
    """Serves the login page and handles the post-login redirect."""

    protocol_version = "HTTP/1.1"

    def do_GET(self) -> None:  # noqa: N802 - name fixed by BaseHTTPRequestHandler
        parsed = urlparse(self.path)
        flash = dict(parse_qsl(parsed.query)).get("flash")
        if parsed.path in (LOGIN_PATH, "/"):
            self._respond(200, _login_page(flash))
        elif parsed.path == SECURE_PATH:
            self._respond(200, _secure_page(flash))
        else:
            self._respond(404, NOT_FOUND_HTML)

    def do_POST(self) -> None:  # noqa: N802 - name fixed by BaseHTTPRequestHandler
        if urlparse(self.path).path != AUTH_PATH:
            self._respond(404, NOT_FOUND_HTML)
            return
        length = int(self.headers.get("Content-Length", "0"))
        fields = dict(parse_qsl(self.rfile.read(length).decode("utf-8"), keep_blank_values=True))
        username = fields.get("username", "")
        password = fields.get("password", "")

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            self._redirect_with_flash(SECURE_PATH, "You logged into a secure area!")
        elif username != VALID_USERNAME:
            self._redirect_with_flash(LOGIN_PATH, "Your username is invalid!")
        else:
            self._redirect_with_flash(LOGIN_PATH, "Your password is invalid!")

    def _redirect_with_flash(self, path: str, flash: str) -> None:
        self.send_response(302)
        self.send_header("Location", f"{path}?flash={quote(flash)}")
        self.send_header("Content-Length", "0")
        self.end_headers()

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
def serve_the_internet(host: str = "127.0.0.1") -> Iterator[str]:
    """Run the login-flow stand-in on an ephemeral port and yield its base URL."""
    server = ThreadingHTTPServer((host, 0), LoginFlowHandler)
    server.daemon_threads = True
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://{host}:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
