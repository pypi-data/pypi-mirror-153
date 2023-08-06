from rest_framework import exceptions, status
from django.utils.translation import gettext_lazy as _


class InvalidAPIVersion(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Invalid or missing API version")
    default_code = "invalid_api_version"
