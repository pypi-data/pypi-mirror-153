import httpx

from eztea.web._testing import (
    CallResult,
    HttpxTestClient,
)

__all__ = (
    "CallResult",
    "WebTestClient",
)


class WebTestClient(HttpxTestClient):
    def __init__(self, app, *, headers=None, prefix: str = ""):
        transport = httpx.WSGITransport(app=app, raise_app_exceptions=False)
        super().__init__(transport=transport, headers=headers, prefix=prefix)
