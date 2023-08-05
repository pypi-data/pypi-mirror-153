import typing

import httpx
from django.http import HttpResponse
from django.test import Client as _TestClient


class DjangoByteStream(httpx.SyncByteStream):
    def __init__(self, response: HttpResponse) -> None:
        self._response = response

    def __iter__(self) -> typing.Iterator[bytes]:
        for part in self._response:
            yield part


class DjangoTestingTransport(httpx.BaseTransport):
    """
    A httpx transport for django testing, based on django.test.Client.
    """

    def __init__(self) -> None:
        self.__client = _TestClient(raise_request_exception=False)

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        handler = getattr(self.__client, request.method.lower())
        # see also: httpx._transport.wsgi.WSGITransport
        environ = {
            "QUERY_STRING": request.url.query.decode("ascii"),
        }
        for header_key, header_value in request.headers.raw:
            key = header_key.decode("ascii").upper().replace("-", "_")
            if key not in ("CONTENT_TYPE", "CONTENT_LENGTH"):
                key = "HTTP_" + key
            environ[key] = header_value.decode("ascii")
        if request.method in ("POST", "PUT", "PATCH", "DELETE", "OPTIONS"):
            content = request.read()
            if content:
                environ["content_type"] = ""
                environ["data"] = content
        result: HttpResponse = handler(request.url.path, **environ)
        headers = list(result.headers.items())
        stream = DjangoByteStream(result)
        response = httpx.Response(
            result.status_code, headers=headers, stream=stream
        )
        return response
