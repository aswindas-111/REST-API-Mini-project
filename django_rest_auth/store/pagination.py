from rest_framework import pagination


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 5
    max_page_size=3
    page_size_query_param='count'
    page_query_param='p'