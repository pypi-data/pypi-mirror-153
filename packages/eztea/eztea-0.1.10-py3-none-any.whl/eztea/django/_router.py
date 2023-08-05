import logging
from collections import ChainMap
from typing import Callable, Dict, List

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import URLPattern
from django.urls import path as url_path
from django.views import View
from validr import Invalid

import eztea.json as ezjson
from eztea.web._mimetype import MIME_TYPE_JSON, MIME_TYPE_MULTIPART
from eztea.web._router import BaseRouter, RouterHandlerDefine
from eztea.web.error import (
    BaseWebError,
    RequestParamsInvalid,
    ResponderReturnsInvalid,
)

LOG = logging.getLogger(__name__)


class BaseRouterAdapter:
    def extract_params(
        self,
        req: HttpRequest,
        kwargs: dict,
    ) -> dict:
        """Extract parameters from request"""
        data_s = [kwargs]
        if req.content_type == MIME_TYPE_JSON:
            data_s.append(ezjson.loads(req.body))
        elif req.content_type == MIME_TYPE_MULTIPART:
            data_s.append(self._extract_multipart(req))
        else:
            data_s.append(req.POST)
        data_s.append(req.GET)
        return ChainMap(*data_s)

    def _is_json_str(self, value: str):
        value = value.strip()
        for start, end in ("{}", "[]", '""'):
            if value.startswith(start) and value.endswith(end):
                return True
        return False

    def _try_decode_json(self, value: str):
        if self._is_json_str(value):
            try:
                value = ezjson.loads(value)
            except ezjson.JSONDecodeError:
                pass  # ignore
        return value

    def _extract_multipart(self, request: HttpRequest):
        params = {}
        for name, file_info in request.FILES.items():
            data = file_info.read()
            params[name] = dict(
                filename=file_info.name,  # TODO: secure filename
                content_type=file_info.content_type,
                data=data,
            )
        # FIX: django not decode multipart content by content-type, and
        # not able to access the multipart content-type, so try decode json
        # and fallback to plain text if failed.
        for name, value in request.POST.items():
            params[name] = self._try_decode_json(value)
        return params

    def error_response(
        self,
        req: HttpRequest,
        error: BaseWebError,
    ) -> HttpResponse:
        """Create error response"""
        response = JsonResponse(
            {
                "error": error.error,
                "message": error.message,
                "detail": error.detail,
            },
            safe=False,
            status=error.status,
        )
        header_items = getattr(error.headers, "items", None)
        if callable(header_items):
            headers = header_items()
        else:
            headers = error.headers or []
        for name, value in headers:
            response[name] = value
        return response

    def success_response(
        self,
        req: HttpRequest,
        returns: dict,
    ) -> HttpResponse:
        """Create success response"""
        if returns is not None:
            if not isinstance(returns, HttpResponse):
                returns = JsonResponse(returns, safe=False)
        else:
            returns = HttpResponse(status=204)
        return returns


class RouterHandler:
    def __init__(
        self,
        define: RouterHandlerDefine,
        adapter: BaseRouterAdapter,
    ) -> None:
        self._define = define
        self._adapter = adapter

    def _extract_params(self, request: HttpRequest, kwargs: dict) -> dict:
        request_data = self._adapter.extract_params(request, kwargs=kwargs)
        try:
            params = self._define.validate_params(request_data)
        except Invalid as ex:
            raise RequestParamsInvalid(ex) from ex
        return params

    def on_request(self, request: HttpRequest, **kwargs) -> HttpRequest:
        try:
            if self._define.validate_params is not None:
                params = self._extract_params(request, kwargs)
            else:
                params = kwargs
            returns = self._define.func(request, **params)
            if self._define.validate_returns is not None:
                try:
                    returns = self._define.validate_returns(returns)
                except Invalid as ex:
                    raise ResponderReturnsInvalid(str(ex)) from ex
            return self._adapter.success_response(request, returns=returns)
        except BaseWebError as ex:
            request_line = f'{request.method} {request.path}'
            LOG.info(f'{request_line} {ex.error} {ex.message}')
            return self._adapter.error_response(request, error=ex)


class Router(BaseRouter):
    def __init__(
        self,
        *,
        decorators: list = None,
        adapter: BaseRouterAdapter = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.__decorators = decorators or []
        self.__adapter = adapter or BaseRouterAdapter()

    def __make_view(
        self,
        handler_define_s: Dict[str, RouterHandlerDefine],
    ) -> Callable[..., HttpResponse]:
        class RouterView(View):
            pass

        for method, define in handler_define_s.items():
            handler = RouterHandler(define, adapter=self.__adapter)
            setattr(RouterView, f"{method.lower()}", handler.on_request)
        view = RouterView.as_view()
        for decorator in reversed(self.__decorators):
            view = decorator(view)
        return view

    def to_url_s(self) -> List[URLPattern]:
        url_s = []
        for path, handler_define_s in self._define_s.items():
            view = self.__make_view(handler_define_s)
            url_s.append(url_path(path.lstrip("/"), view))
        return url_s
