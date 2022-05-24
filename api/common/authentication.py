from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models.user import User


class PuppyAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = User

    def get_raw_token(self, header):
        return header


