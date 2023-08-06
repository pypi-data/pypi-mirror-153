from typing import Any, Optional
from rest_framework.response import Response
from rest_framework.test import APIClient


class BaseAPIClient(APIClient):
    """
    Utility base API client used in tests to carry versioning information.
    I have purposefully ignored mypy warnings about method signature because the
    overrides chain defined in rest_framework is not consistent.
    """

    ACCEPT_HEADER = ""

    def get(self, path: str, **extra: Any) -> Response:  # type: ignore[override]
        return super().get(path, HTTP_ACCEPT=self.ACCEPT_HEADER, **extra)

    def post(self, path: str, data: Optional[Any], **extra: Any) -> Response:  # type: ignore[override]
        return super().post(path, data=data, HTTP_ACCEPT=self.ACCEPT_HEADER, **extra)

    def patch(self, path: str, data: Optional[Any], **extra: Any) -> Response:  # type: ignore[override]
        return super().patch(path, data=data, HTTP_ACCEPT=self.ACCEPT_HEADER, **extra)

    def delete(self, path: str, **extra: Any) -> Response:  # type: ignore[override]
        return super().delete(path, HTTP_ACCEPT=self.ACCEPT_HEADER, **extra)


class APIClientV1_0(BaseAPIClient):
    ACCEPT_HEADER = "application/json"
