

from rest_framework.pagination import PageNumberPagination


class SmallResultsSetPagination(PageNumberPagination):

    page_size = 10
    max_page_size = 10
    page_query_param = 'page_size'
