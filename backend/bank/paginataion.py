# DRF
from rest_framework.pagination import PageNumberPagination


class BasePaginator(PageNumberPagination):
    """
    Simple pagination of data.
    """
    # Size of query on the page
    page_size = 15

    def get_paginated_response(self, data):
        """
        Return paginated response.
        """
        return {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        }
