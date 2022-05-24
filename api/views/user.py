from rest_framework import mixins, viewsets, decorators, response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.datastructures import MultiValueDictKeyError
from api.common.authentication import PuppyAuthentication
from api.common.permissions import IsAuthenticatedPermission
from api.common.responses import fail_response
from api.common.exceptions import client_error
from api.views.base import BaseView
from api.seralizers.user import UserSerializer
from api.models.user import User


class UserViewSet(BaseView,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    authentication_classes = [PuppyAuthentication]
    permission_classes = [IsAuthenticatedPermission]
    serializer_class = UserSerializer
    pagination_class = None
    queryset = User.objects.all()

    @decorators.action(methods=['post'], detail=False, permission_classes=[], authentication_classes=[])
    def login(self, request):
        try:
            phone = request.data['phone']
            code = request.data['code']
            user = User.objects.get(phone=phone)
        except MultiValueDictKeyError as e:
            return fail_response(client_error(f'参数{str(e)}不能为空'))
        except User.DoesNotExist:
            user = User(phone=phone)
            user.save()
        token = RefreshToken.for_user(user)
        return response.Response({'token': str(token.access_token), 'user': UserSerializer(user).data})

    @decorators.action(methods=['post'], detail=False, permission_classes=[])
    def logout(self, request):
        return response.Response()
