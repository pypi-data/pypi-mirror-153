from rest_framework.response import Response
from ..constants import ERROR_CODE
from ..misc import create_api_error


def generic_error(status: int, error_code: ERROR_CODE, error_message: str) -> Response:
    return Response(status=status, data=create_api_error(error_code, error_message))
