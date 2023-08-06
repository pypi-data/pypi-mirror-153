from rest_framework.pagination import PageNumberPagination as _PageNumberPagination, \
    LimitOffsetPagination as _LimitOffsetPagination, CursorPagination as _CursorPagination, _positive_int

from djackal.settings import djackal_settings


class BasePagination:
    def get_paginated_meta(self):
        raise NotImplementedError('get_paginated_meta() must be implemented.')


class PageNumberPagination(BasePagination, _PageNumberPagination):
    page_size = djackal_settings.PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = djackal_settings.MAX_PAGE_SIZE

    def get_paginated_meta(self):
        return {
            'count': self.page.paginator.count,
            'page': self.page.number,
        }


class LimitOffsetPagination(BasePagination, _LimitOffsetPagination):
    def get_paginated_meta(self):
        return {
            'count': self.count,
            'previous': self.get_previous_link(),
            'next': self.get_next_link(),
        }


class CursorPagination(BasePagination, _CursorPagination):
    def get_paginated_meta(self):
        return {
            'previous': self.get_previous_link(),
            'next': self.get_next_link(),
        }


class NoCountPagination(PageNumberPagination):
    last_page_strings = None

    def get_page_number(self, request):
        if self.page_size_query_param:
            try:
                return _positive_int(
                    request.query_params[self.page_query_param],
                )
            except (KeyError, ValueError):
                pass

        return 1

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        page_number = self.get_page_number(request)

        offset = page_size * (page_number - 1)

        # Get one extra element to check if there is a "next" page
        q = list(queryset[offset: offset + page_size + 1])
        self.count = offset + len(q) if len(q) else offset - 1
        self.has_next = False

        if len(q) > page_size:
            self.has_next = True
            q.pop()

        self.request = request
        return q

    def get_paginated_meta(self):
        return {
            'has_next': self.has_next
        }
