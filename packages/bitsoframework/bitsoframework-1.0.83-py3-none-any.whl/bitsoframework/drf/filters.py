from django_filters.rest_framework import BaseInFilter, CharFilter


class InListFilter(BaseInFilter, CharFilter):
    pass
