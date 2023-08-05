from django.http import HttpRequest
from django.core.cache import cache
from django.conf import settings
from django.utils.translation import gettext as _
from .results import ApiResult
from typing import List, Set
import json
from knifes import aes
import pickle


def login_required(view_func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if settings.TOKEN_KEY not in request.headers or not request.headers[settings.TOKEN_KEY]:
            return ApiResult.tokenInvalid()
        request.token = request.headers[settings.TOKEN_KEY]
        data = cache.get(settings.TOKEN_KEY + request.token)
        if not data:
            return ApiResult.tokenInvalid()
        # 只能反序列化简单类型数据
        request.user = pickle.loads(data)
        return view_func(request, *args, **kwargs)
    return wrapper


def params_required(param_keys: List, is_get=False):
    def outer_wrapper(view_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if param_keys and is_get:
                for param_key in param_keys:
                    if param_key not in request.GET or not request.GET[param_key]:
                        return ApiResult.missingParam()
            elif param_keys:
                for param_key in param_keys:
                    if param_key not in request.POST or not request.POST[param_key]:
                        return ApiResult.missingParam()
            return view_func(request, *args, **kwargs)
        return wrapper
    return outer_wrapper


def decrypt_and_check_params(param_keys: Set = None, header_param_keys: Set = None):
    if param_keys is None:
        param_keys = {'timestamp'}
    else:
        param_keys.add('timestamp')
    def outer_wrapper(view_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if not request.body:
                return ApiResult.missingParam()
            request.params = json.loads(request.body)
            encrypt_params = {}
            is_online = not request.headers.get('vi-test')
            if is_online:
                encrypt_params = json.loads(aes.decrypt(request.params.get('vs'), settings.AES_BODY_KEY))

            # 检查参数   TODO 判断timestamp是否过期
            for param_key in param_keys:
                if param_key not in request.params:
                    return ApiResult.missingParam()
                if is_online and request.params.get(param_key) != encrypt_params.get(param_key):  # online环境校验
                    return ApiResult.missingParam(_('参数非法'))

            if not request.headers.get('vi'):
                ApiResult.missingParam()
            request.header_params = json.loads(aes.decrypt(request.headers.get('vi'), settings.AES_HEADER_KEY))
            # 检查参数
            if header_param_keys:
                for header_param in header_param_keys:
                    if header_param not in request.header_params:
                        return ApiResult.missingParam()
            return view_func(request, *args, **kwargs)
        return wrapper
    return outer_wrapper


def decrypt_and_check_body_params(param_keys: Set = None):
    if param_keys is None:
        param_keys = {'timestamp'}
    else:
        param_keys.add('timestamp')
    def outer_wrapper(view_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if not request.body:
                return ApiResult.missingParam()
            request.params = json.loads(request.body)
            encrypt_params = {}
            is_online = not request.headers.get('vi-test')
            if is_online:
                encrypt_params = json.loads(aes.decrypt(request.params.get('vs'), settings.AES_BODY_KEY))

            # 检查参数   TODO 判断timestamp是否过期
            for param_key in param_keys:
                if param_key not in request.params:
                    return ApiResult.missingParam()
                if is_online and request.params.get(param_key) != encrypt_params.get(param_key):  # online环境校验
                    return ApiResult.missingParam(_('参数非法'))
            return view_func(request, *args, **kwargs)
        return wrapper
    return outer_wrapper


def decrypt_and_check_header_params(header_param_keys: Set = None):
    def outer_wrapper(view_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if not request.headers.get('vi'):
                ApiResult.missingParam()
            request.header_params = json.loads(aes.decrypt(request.headers.get('vi'), settings.AES_HEADER_KEY))
            # 检查参数
            if header_param_keys:
                for header_param in header_param_keys:
                    if header_param not in request.header_params:
                        return ApiResult.missingParam()
            return view_func(request, *args, **kwargs)
        return wrapper
    return outer_wrapper


# json请求 参数校验
def decode_and_check_body_params(param_keys: Set = None):
    def outer_wrapper(view_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if not request.body:
                return ApiResult.missingParam()
            request.params = json.loads(request.body)
            # 检查参数
            for param_key in param_keys:
                if param_key not in request.params:
                    return ApiResult.missingParam()
            return view_func(request, *args, **kwargs)
        return wrapper
    return outer_wrapper
