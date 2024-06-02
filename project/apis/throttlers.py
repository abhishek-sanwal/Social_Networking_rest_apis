
from rest_framework.throttling import ScopedRateThrottle, UserRateThrottle


class SendApiThrottle(UserRateThrottle):

    rate = '3/minute'

    def allow_request(self, request, view):

        return super().allow_request(request, view)
