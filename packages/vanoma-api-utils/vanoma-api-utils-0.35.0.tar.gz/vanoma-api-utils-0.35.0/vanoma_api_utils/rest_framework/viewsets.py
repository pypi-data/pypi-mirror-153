from rest_framework import viewsets
from .generics import GenericAPIView


class GenericViewSet(viewsets.ViewSetMixin, GenericAPIView):
    """
    Similar to DRF's viewsets.GenericViewSet except we inherit from our custom
    GenericAPIView to resolve serializer class based on the requested API version.
    """
