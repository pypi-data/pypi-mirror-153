from typing import Callable, Dict, List, Optional, Union

from validr import Builder, Compiler, Schema

from ._signature import get_params, get_returns

ALL_HTTP_METHODS = (
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "PATCH",
    "HEAD",
    "OPTIONS",
    "TRACE",
)


def _normalize_methods(methods: Optional[List[str]]):
    methods = [x.upper() for x in methods or ALL_HTTP_METHODS]
    unknown_methods = set(methods) - set(ALL_HTTP_METHODS)
    if unknown_methods:
        msg = ", ".join(unknown_methods)
        raise ValueError(f"unknown http method {msg}")
    return methods


class RouterHandlerDefine:
    def __init__(
        self,
        func: Callable,
        path: str,
        methods: List[str],
        description: Optional[str],
        validate_params: Optional[Union[Schema, Callable]],
        validate_returns: Optional[Union[Schema, Callable]],
    ) -> None:
        self.func = func
        self.path = path
        self.methods = methods
        self.description = description
        self.validate_params = validate_params
        self.validate_returns = validate_returns


class BaseRouter:
    def __init__(self, *, schema_compiler: Compiler = None) -> None:
        self._schema_compiler = schema_compiler or Compiler()
        # dict: path -> method -> define
        self._define_s: Dict[str, Dict[str, RouterHandlerDefine]] = {}

    def _add_handler_define(self, define: RouterHandlerDefine):
        action_define_s = self._define_s.setdefault(define.path, {})
        for method in define.methods:
            if method in action_define_s:
                msg = f"duplicated route {method} {define.path}"
                raise ValueError(msg)
            action_define_s[method] = define

    def route(
        self,
        path: str,
        methods: List[str] = None,
        params: Union[Schema, Builder] = None,
    ):
        methods = _normalize_methods(methods)

        def decorator(fn):
            fn_params = params
            if fn_params is None:
                fn_params = get_params(fn)
            fn_returns = get_returns(fn)
            _validate_params = None
            if fn_params is not None:
                _validate_params = self._schema_compiler.compile(fn_params)
            _validate_returns = None
            if fn_returns is not None:
                _validate_returns = self._schema_compiler.compile(fn_returns)
            self._add_handler_define(
                RouterHandlerDefine(
                    func=fn,
                    path=path,
                    methods=methods,
                    validate_params=_validate_params,
                    validate_returns=_validate_returns,
                    description=fn.__doc__,
                )
            )
            return fn

        return decorator

    def get(self, path: str, params: Union[Schema, Builder] = None):
        return self.route(path, methods=["GET"], params=params)

    def post(self, path: str, params: Union[Schema, Builder] = None):
        return self.route(path, methods=["POST"], params=params)

    def put(self, path: str, params: Union[Schema, Builder] = None):
        return self.route(path, methods=["PUT"], params=params)

    def delete(self, path: str, params: Union[Schema, Builder] = None):
        return self.route(path, methods=["DELETE"], params=params)

    def patch(self, path: str, params: Union[Schema, Builder] = None):
        return self.route(path, methods=["PATCH"], params=params)

    def head(self, path: str, params: Union[Schema, Builder] = None):
        return self.route(path, methods=["HEAD"], params=params)

    def options(self, path: str, params: Union[Schema, Builder] = None):
        return self.route(path, methods=["OPTIONS"], params=params)

    def trace(self, path: str, params: Union[Schema, Builder] = None):
        return self.route(path, methods=["TRACE"], params=params)
