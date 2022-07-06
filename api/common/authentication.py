from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models.user.user import User
from api.common.exceptions import ERROR_CODE_1001


class PuppyAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = User

    def get_raw_token(self, header):
        return header

    def get_user(self, validated_token):
        user = super(PuppyAuthentication, self).get_user(validated_token)
        if user.is_blocking:
            raise ERROR_CODE_1001
        return user

