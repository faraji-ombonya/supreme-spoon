from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "per_page"
    max_page_size = 100

    def get_paginated_response(self, data):
        return {
            "page": self.page.number,
            "per_page": self.page.paginator.per_page,
            "count": self.page.paginator.count,
            "results": data,
        }


def paginate(qs, serializer_class, request):
    """Paginate a queryset and return a paginated response.

    Args:
        qs (QuerySet): The QuerySet to paginate.
        serializer_class: Serializer class to serialize response.
        request (Request): request

    Returns:
        response: A paginated response.
    """
    paginator = Pagination()
    paginated_qs = paginator.paginate_queryset(qs, request)
    serializer = serializer_class(paginated_qs, many=True)
    response = paginator.get_paginated_response(serializer.data)
    return response
