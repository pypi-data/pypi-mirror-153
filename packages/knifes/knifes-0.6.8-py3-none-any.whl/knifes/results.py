from __future__ import annotations
from django.http import JsonResponse
from django.utils.translation import gettext as _
from .jsons import ObjectEncoder
from typing import Optional
from enum import Enum


class BaseErrorEnum(Enum):
    """
    error code is negative number
    """
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg

    @classmethod
    def get_by_code(cls, code) -> Optional[BaseErrorEnum]:
        return next(filter(lambda x: x.code == code, cls.__members__.values()), None)


class ApiResult:
    code = 200
    succ = True
    msg = ''
    msg_detail = ''
    data = None

    @classmethod
    def fail(cls, msg, code=400, msg_detail=None):
        ret = ApiResult()
        ret.succ = False
        ret.code = code
        ret.msg = msg
        ret.msg_detail = msg_detail
        return ret

    @classmethod
    def succ(cls, data=None):
        ret = ApiResult()
        ret.code = 200
        ret.succ = True
        ret.data = data
        return ret

    @classmethod
    def succResponse(cls, data=None):
        return JsonResponse(cls.succ(data), encoder=ObjectEncoder, safe=False)

    @classmethod
    def failResponse(cls, msg, code=400, msg_detail=None):
        return JsonResponse(cls.fail(msg, code=code, msg_detail=msg_detail), encoder=ObjectEncoder, safe=False)

    @classmethod
    def errorResponse(cls, error_enum: BaseErrorEnum, msg_detail=None):
        return JsonResponse(cls.fail(error_enum.msg, code=error_enum.code, msg_detail=msg_detail), encoder=ObjectEncoder, safe=False)

    @classmethod
    def tokenInvalid(cls, msg=_('请先登录')):
        return cls.failResponse(msg, code=300)

    @classmethod
    def missingParam(cls, msg=_('缺少参数')):
        return cls.failResponse(msg)
