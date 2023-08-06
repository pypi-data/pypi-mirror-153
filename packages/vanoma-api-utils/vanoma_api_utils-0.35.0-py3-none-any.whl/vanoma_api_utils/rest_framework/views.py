import logging
import humps
from typing import Any, Dict
from django.http import Http404
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import set_rollback
from vanoma_api_utils.constants import ERROR_CODE
from .responses import generic_error


def _extract_message_from_detail(detail: Any) -> str:
    if isinstance(detail, list):
        errors = [_extract_message_from_detail(d) for d in detail]
        return ",".join(errors)
    elif isinstance(detail, dict):
        errors = [
            f"{humps.camelize(k)}: {_extract_message_from_detail(v)}"
            for k, v in detail.items()
        ]
        return " ".join(errors)
    else:
        return str(detail)


def exception_handler(exc: Exception, context: Dict[str, Any]) -> Response:
    """
    Mostly copied from https://github.com/encode/django-rest-framework/blob/master/rest_framework/views.py#L71
    """
    if isinstance(exc, Http404) or isinstance(exc, ObjectDoesNotExist):
        return generic_error(
            status.HTTP_404_NOT_FOUND,
            ERROR_CODE.RESOURCE_NOT_FOUND,
            str(exc),
        )

    if isinstance(exc, PermissionDenied):
        return generic_error(
            status.HTTP_403_FORBIDDEN,
            ERROR_CODE.AUTHORIZATION_ERROR,
            str(exc),
        )

    if isinstance(exc, exceptions.APIException):
        set_rollback()
        return generic_error(
            exc.status_code,
            ERROR_CODE.INVALID_REQUEST,
            _extract_message_from_detail(exc.detail),
        )

    # This will sent the current exception to sentry - https://docs.sentry.io/platforms/python/guides/logging/
    logging.exception(str(exc))

    return generic_error(
        status.HTTP_500_INTERNAL_SERVER_ERROR, ERROR_CODE.INTERNAL_ERROR, str(exc)
    )
