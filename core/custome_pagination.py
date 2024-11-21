from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10  # Default page size, adjust as needed
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        # Calculate total pages
        total_pages = self.page.paginator.num_pages
        # Get the current page number
        current_page = self.page.number
        # Get the page size
        page_size = self.page_size
        total_recored_count = self.page.paginator.count
        
        return Response(
            data={
                'page_no': current_page,
                'total_pages': total_pages,
                'items_per_page': page_size,
                'total_no_of_records': total_recored_count,
                'url': self.request.build_absolute_uri(),  # Current URL
                'next': self.get_next_link(),  # URL for the next page
                'previous': self.get_previous_link(),  # URL for the previous page
                'results': data
            },
        )
