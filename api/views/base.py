import http

from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from api.common.exceptions import SaoException, ERROR_CODE_1000
from api.common.responses import fail_response, FailResponse
from django.http.response import Http404


class BaseView(APIView):
    def initialize_request(self, request, *args, **kwargs):
        request.method = request.method.lower()
        return super(BaseView, self).initialize_request(request, *args, **kwargs)

    def handle_exception(self, exc):
        print(type(exc))
        print(exc)
        if isinstance(exc, (exceptions.NotAuthenticated, exceptions.AuthenticationFailed)):
            return fail_response(ERROR_CODE_1000)
        elif isinstance(exc, SaoException):
            return fail_response(exc)
        elif isinstance(exc, APIException):
            return fail_response(SaoException(code=1007, msg=str(exc.detail)))
        elif isinstance(exc, Http404):
            return fail_response(SaoException(code=1006, msg=str(exc)))
        else:
            http_status = http.HTTPStatus.INTERNAL_SERVER_ERROR
            try:
                response = super(BaseView, self).handle_exception(exc)
                http_status = response.status_code
            except:
                http_status = http.HTTPStatus.INTERNAL_SERVER_ERROR
            finally:
                return fail_response(SaoException(code=1007, msg=str(exc)), http_status=http_status)

    def finalize_response(self, request, response, *args, **kwargs):
        if not isinstance(response, FailResponse):
            response.data = {
                'code': 0,
                'message': 'ok',
                'data': response.data
            }
        return super(BaseView, self).finalize_response(request, response, *args, **kwargs)
