import uuid

from qiniu import Auth
from rest_framework import decorators, request
from api.common.authentication import PuppyAuthentication
from api.common.permissions import IsAuthenticatedPermission
from api.common.responses import success_response
from manage import environment, Environment
from time import time
from api.models.support import IdAndName
from uuid import uuid3

access_key = 'SbwkTlo_6Z1VdYRNY_XkRmPRIUFg8PmqAagEMlxr'
secret_key = 'ucf8mWaW8v0QfBHsriRV816TD0jWjiu3nYiCFlYr'

q = Auth(access_key, secret_key)

timeout = 3600

upload_image_policy = {
    'mimeLimit': 'image/jpeg'
}


def get_bucket_name():
    match environment:
        case Environment.PRODUCT:
            return 'puppy-product'
        case _:
            return 'puppy-develop'


@decorators.api_view(http_method_names=['GET'])
@decorators.authentication_classes([PuppyAuthentication])
@decorators.permission_classes([IsAuthenticatedPermission])
def get_upload_tokens(req: request.Request):
    """
    获取文件上传的 token
    返回包含文件名和token的数组. 前端使用该文件名+文件扩展名和token进行上传.
    上传图片: 只能使用jpeg格式. mime为image/jpeg
    """
    count = req.query_params.get('count', None)
    if not count:
        return success_response([])

    user_id = req.user.pk
    timestamp = int(time())
    bucket_name = get_bucket_name()
    tokens = []
    for i in range(int(count)):
        key = uuid3(uuid.NAMESPACE_DNS, f'{user_id}{timestamp}{i}').hex
        token = q.upload_token(bucket_name, key, timeout)
        tokens.append(IdAndName(key, token)._asdict())
    return success_response(tokens)
