from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    queryset = None
    values = []
    fields = []

    def paginate_queryset(self, queryset, request, view=None):
        self.queryset = queryset
        return super().paginate_queryset(queryset, request, view)

    def get_queryset(self):
        assert self.queryset is not None, 'queryset is not None'
        return self.queryset

    def set_values(self):
        self.values = [(field, getattr(self, field)())
                       for field in self.fields]

    def get_paginated_response(self, data):
        self.set_values()
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            *self.values
        ]))
