from threading import local

_active = local()


def get_params(request=None):
    request = request or get_request()

    if hasattr(request, 'data') and request.data:
        return request.data

    return request.POST or request.GET


def get_param(name, request=None, default=None):
    request = request or get_request()

    if name in request.GET:
        return request.GET.get(name, default)

    if name in request.POST:
        return request.POST.get(name, default)

    if hasattr(request, 'data') and request.data and name in request.data:
        return request.data.get(name, default)

    return default


def set_request(user, **kwargs):
    from rest_framework.request import Request
    from django.http.request import HttpRequest
    _active.request = Request(HttpRequest(**kwargs))
    _active.request.user = user
    return _active.request


def get_request():
    """
    Utility that gets the current request
    """

    if hasattr(_active, "request"):

        return _active.request
    else:
        return None


def get_user():
    """
    Utility that safely gets the current logged user (when using
    GlobalRequestMiddleware).
    """
    request = get_request()

    if request and request.user.is_authenticated:
        return request.user

    return None


def get_agent():
    """
    Utility that safely gets the current requestor's user agent (when using
    GlobalRequestMiddleware).
    """
    request = get_request()

    if request and request.META:
        return request.META.get("HTTP_USER_AGENT")

    return None


class GlobalRequestMiddleware(object):
    """
    Midlware that attaches the current request into the local thread and makes
    it available via #get_request() function.

    MIDDLEWARE_CLASSES = (
        ...
        'bitso.middleware.GlobalRequestMiddleware'
        ...
    )

    @author: bitsoframework
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        _active.request = request
        return None
