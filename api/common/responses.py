from rest_framework.response import Response
from api.common.exceptions import ERROR_CODE_0, SaoException


class FailResponse(Response):
    pass


def success_response(data=None) -> Response:
    return Response({'code': ERROR_CODE_0.code, 'message': ERROR_CODE_0.msg, 'data': data})


def fail_response(exception: SaoException, http_status: int = None) -> Response:
    return FailResponse({'code': exception.code, 'message': exception.msg},
                        status=http_status if http_status else exception.get_http_status())
