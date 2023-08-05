from typing import TypeVar
from django.http import HttpRequest
import logging
T = TypeVar('T')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_request_param_strip_spaces(request: HttpRequest, key):
    value = request.POST.get(key, request.GET.get(key))
    return value.strip() if value else value


def get_object_or_None(T, **kwargs) -> T:
    objs = T.objects.filter(**kwargs)
    if objs:
        return objs[0]
    return None


class OnlyDebugLevel(logging.Filter):
    def filter(self, record):
        return record.levelname == 'DEBUG'
