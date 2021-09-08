from collections import OrderedDict
from urllib.parse import urlparse, parse_qsl

from rest_framework.pagination import CursorPagination,PageNumberPagination
from rest_framework.response import Response


class CursorIdPagination(CursorPagination):
    ordering = '-pk'
    page_size = 20
    cursor_query_param = 'next_cursor'

    def get_paginated_response(self, data, **extra_data):
        next_url = self.get_next_link()
        if next_url:
            parsed = urlparse(next_url)
            cursor = dict(parse_qsl(parsed.query))['next_cursor']
        else:
            cursor = ''
        result_dict = OrderedDict([
            ('next', self.get_next_link()),
            ('next_cursor', cursor),
            ('data', data)])
        result_dict.update(extra_data)
        return Response(result_dict)


class PageIDPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    page_query_param = "page_id"
    max_page_size = 100

    def get_paginated_response(self, data, **extra_data):
        result_dict = OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)])
        result_dict.update(extra_data)
        return Response(result_dict)