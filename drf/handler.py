import logging

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.views import set_rollback

from core.exceptions import BusinessException, EXCEPTION_PARAMETER_FORMAT_ERROR
from .response import error_response

logger = logging.getLogger("django")


def business_exception_handler(exc, context):
    set_rollback()
    return error_response(exc.code, exc.message, exc.data, exc.app)


def exception_handler(exc, context):
    """异常接收处理器"""

    if isinstance(exc, BusinessException):
        return business_exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        error_message = list(dict(exc.detail).values())[0]
        if isinstance(error_message, list):
            error_message = error_message[0]
        elif isinstance(error_message, dict):
            error_message = list(dict(error_message).values())
        else:
            error_message = None
        return error_response(
            EXCEPTION_PARAMETER_FORMAT_ERROR,
            error_message,
            data=exc.detail,
            app=getattr(exc, "app", None),
        )

    if isinstance(exc, Http404):
        api_exception = BusinessException(code=404, message="找不到对应的数据详情")
        return business_exception_handler(api_exception, context)

    if isinstance(exc, PermissionDenied):
        api_exception = BusinessException(code=403, message="当前用户的权限不够")
        return business_exception_handler(api_exception, context)

    if isinstance(exc, APIException):
        api_exception = BusinessException(
            code=exc.status_code, message=exc.default_detail, data=exc.detail
        )
        return business_exception_handler(api_exception, context)

    # 是否直接抛出严重的错误，线上环境会关闭此配置
    AI_APPLET_SERIOUS_ERROR = getattr(settings, "AI_APPLET_SERIOUS_ERROR", True)
    if not AI_APPLET_SERIOUS_ERROR:
        try:
            # 如果有设置 sentry，日志打到对应的 sentry 中
            # TODO:需要安装 sentry 服务
            # sentry_client.captureException()
            pass
        except Exception:
            pass

        # 如果是非开发环境，则返回对应的错误，而不是直接报 500
        return business_exception_handler(BusinessException(data=str(exc)), context)
