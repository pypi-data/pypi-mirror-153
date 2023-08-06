from typing import Any
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from djangorestframework_camel_case.settings import api_settings  # type: ignore
from djangorestframework_camel_case.util import underscoreize  # type: ignore


class CamelCaseMiddleWare:
    """
    Middleware to convert camelCase query params to snake_case. Copied from https://github.com/vbabiy/djangorestframework-camel-case/pull/68
    """

    def __init__(self, get_response: Any) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request.GET = underscoreize(request.GET, **api_settings.JSON_UNDERSCOREIZE)

        response = self.get_response(request)
        return response
