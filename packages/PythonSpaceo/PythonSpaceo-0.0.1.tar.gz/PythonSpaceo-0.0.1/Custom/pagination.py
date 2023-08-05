from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'TotalCount': self.page.paginator.count,
            'ResponseMessage': 'Success!!',
            'results': data,
            'links': {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            }
        })
