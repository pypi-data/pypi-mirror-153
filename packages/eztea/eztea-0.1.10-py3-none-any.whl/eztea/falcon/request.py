import cgi
from functools import cached_property

import falcon

from eztea.web._request import FormFile

__all__ = (
    "parse_content_type",
    "Request",
    "FormFile",
)


def parse_content_type(content_type: str):
    if not content_type:
        return ("", {})
    mimetype, params = cgi.parse_header(content_type)
    return mimetype.lower(), params


class Request(falcon.Request):
    @cached_property
    def __content_type_parsed(self):
        return parse_content_type(self.content_type)

    @property
    def mimetype(self):
        """
        Like content_type, but without parameters (eg, without charset,
        type etc.) and always lowercase. For example if the content type is
        text/HTML; charset=utf-8 the mimetype would be 'text/html'.
        """
        return self.__content_type_parsed[0]

    @property
    def mimetype_params(self):
        """
        The mimetype parameters as dict. For example if the content type is
        text/html; charset=utf-8 the params would be {'charset': 'utf-8'}.
        """
        return self.__content_type_parsed[1]
