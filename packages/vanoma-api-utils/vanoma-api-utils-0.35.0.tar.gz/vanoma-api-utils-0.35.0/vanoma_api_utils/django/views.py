from typing import Any
from django.http.response import JsonResponse
from rest_framework import status


def create_root_view(api_name: str) -> Any:
    def root_view(*args: Any, **kwargs: Any) -> JsonResponse:
        return JsonResponse(
            {"name": f"Vanoma {api_name.capitalize()} API"}, status=status.HTTP_200_OK
        )

    return root_view
