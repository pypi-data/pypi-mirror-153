from django_filters import rest_framework as filters  # type: ignore


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass
