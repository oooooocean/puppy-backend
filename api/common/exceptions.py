import http.client as ht


class SaoException(Exception):
    def __init__(self, msg, code, detail=None):
        self.code = code
        self.msg = msg
        self.detail = detail

    def get_http_status(self):
        match self.code:
            case 0:
                return ht.OK
            case 1000:
                return ht.UNAUTHORIZED
            case 1006:
                return ht.NOT_FOUND
            case 1008:
                return ht.INTERNAL_SERVER_ERROR
            case 1001:
                return ht.UNAUTHORIZED
            case _:
                return ht.BAD_REQUEST


ERROR_CODE_0 = SaoException('ok', 0)
ERROR_CODE_1000 = SaoException('Authorization 缺失', 1000)
ERROR_CODE_1001 = SaoException('账户失效', 1001)
ERROR_CODE_1003 = SaoException('登录过期', 1003)
ERROR_CODE_1006 = SaoException('找不到指定资源', 1006)
ERROR_CODE_1007 = SaoException('客户端入参错误', 1007)
ERROR_CODE_1008 = SaoException('服务端错误', 1008)


def client_error(msg: str) -> SaoException:
    return SaoException(msg, 1007)


def server_error(msg: str) -> SaoException:
    return SaoException(msg, 1008)
