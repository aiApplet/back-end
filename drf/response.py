from rest_framework.response import Response
from core.exceptions import ERROR_PHRASES


def success_response(data=None):
    """成功返回的数据结构"""

    if data is None:
        response_data = {
            "code": 0,
            "message": "",
        }
    else:
        response_data = {
            "code": 0,
            "message": "",
            "result": data,
        }

    return Response(response_data)


def error_response(code, message=None, data=None, app=None):
    """业务异常返回的数据结构"""

    if not message:
        message = ERROR_PHRASES.get(code, "")

    response_data = {
        "code": code,
        "message": message,
        "data": data,
        "app": app,
    }

    return Response(response_data)
