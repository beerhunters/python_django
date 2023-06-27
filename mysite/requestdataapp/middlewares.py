import time

from django.http import HttpRequest, HttpResponseBadRequest


# def set_useragent_on_request_middleware(get_response):
#
#     print('initial call')
#     def middleware(request: HttpRequest):
#
#         print('before get response')
#         request.user_agent = request.META['HTTP_USER_AGENT']
#         response = get_response(request)
#         print('after get response')
#         return response
#
#     return middleware


class CountRequestMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.response_count = 0
        self.exception_count = 0

    def __call__(self, request: HttpRequest):
        self.request_count += 1
        print('requests count', self.request_count)
        response = self.get_response(request)
        self.response_count += 1
        print('responses count', self.response_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exception_count += 1
        print('got', self.exception_count, 'exceptions so far')


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        if ip_address in self.requests:
            last_request_time = self.requests[ip_address]
            if time.time() - last_request_time < 10:  # 10 секунд
                return HttpResponseBadRequest('Too many requests.')
        self.requests[ip_address] = time.time()

        response = self.get_response(request)
        return response

    # class ThrottlingMiddleware:
    #     def __init__(self, get_response):
    #         self.get_response = get_response
    #         self.bucket: dict[str, datetime] = {}
    #         self.rate_ms = settings.THROTTLING_RATE_MS
    #
    #     @classmethod
    #     def get_client_ip(cls, request: HttpRequest):
    #         x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    #         if x_forwarded_for:
    #             ip = x_forwarded_for.split(",")[0]
    #         else:
    #             ip = request.META.get("REMOTE_ADDR")
    #         return ip
    #
    #     def request_is_allowed(self, client_ip: str) -> bool:
    #         now = datetime.utcnow()
    #         last_access = self.bucket.get(client_ip)
    #         if not last_access:
    #             return True
    #         if (now - last_access) > timedelta(milliseconds=self.rate_ms):
    #             return True
    #         return False
    #
    #     def __call__(self, request: HttpRequest):
    #         client_ip = self.get_client_ip(request)
    #         if self.request_is_allowed(client_ip):
    #             response = self.get_response(request)
    #             self.bucket[client_ip] = datetime.utcnow()
    #         else:
    #             response = HttpResponse("Rate limit exceeded", status=HTTPStatus.TOO_MANY_REQUESTS)
    #         return response