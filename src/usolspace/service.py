"""Minimal HTTP service exposing USOL data planes to the web tier.

Stdlib-only (no framework), so it deploys anywhere Python runs. It is the LIVE side of the Space
Twin's "live USOL + initial data load": the client-vue quadrant fetches ``/api/space/quadrant`` (the
Vite ``/api`` proxy strips ``/api`` and forwards to ``/space/quadrant`` here); when this service is up
the cube renders from live USOL, otherwise the client falls back to its shipped initial-load asset.

    usol-serve            # or: python -m usolspace.service   (PORT env, default 8087)

Routing is a pure function (``route``) so it is unit-testable without opening a socket. CORS is
permissive-GET only; this serves public, factual astrometry — no secrets, no writes.
"""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Tuple

from usolspace.nearby_stars import quadrant_payload

Response = Tuple[int, dict]


def route(path: str) -> Response:
    """Map a request path to (status, json-body). Pure; no I/O."""
    clean = path.split("?", 1)[0].rstrip("/") or "/"
    if clean in ("/space/quadrant", "/quadrant"):
        return 200, quadrant_payload()
    if clean in ("/healthz", "/livez", "/"):
        return 200, {"ok": True, "service": "usol", "routes": ["/space/quadrant", "/healthz"]}
    return 404, {"error": "not found", "path": clean}


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: dict) -> None:
        payload = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(payload)))
        self.send_header("access-control-allow-origin", "*")
        self.send_header("cache-control", "public, max-age=60")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:  # noqa: N802 (stdlib API)
        status, body = route(self.path)
        self._send(status, body)

    def log_message(self, *args) -> None:  # keep the console quiet in tests/CI
        pass


def main() -> None:
    port = int(os.environ.get("PORT", "8087"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"usol service on :{port} — GET /space/quadrant, /healthz")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
