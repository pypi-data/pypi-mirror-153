from eztea.web._testing import CallResult, HttpxTestClient

from ._wsgi import DjangoTestingTransport

__all__ = (
    "CallResult",
    "WebTestClient",
)


class WebTestClient(HttpxTestClient):
    def __init__(self, app, *, headers=None, prefix: str = ""):
        transport = DjangoTestingTransport()
        super().__init__(transport=transport, headers=headers, prefix=prefix)
