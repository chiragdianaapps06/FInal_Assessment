from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "limit"
    max_page_size = 100
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response(
            {
                
                "current_page": self.page.number,
                "total_count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "data": data,
            }
        )