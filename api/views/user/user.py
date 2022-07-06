from rest_framework import mixins, viewsets, decorators, response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.datastructures import MultiValueDictKeyError
from api.common.authentication import PuppyAuthentication
from api.common.permissions import IsAuthenticatedPermission
from api.common.responses import fail_response
from api.common.exceptions import client_error, ERROR_CODE_1001
from ..base import BaseView
from api.models.user.user import LoginUserSerializer, User, UserSerializer
from api.models.post.post import PostSerializer
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


class UserViewSet(BaseView,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    authentication_classes = [PuppyAuthentication]
    permission_classes = [IsAuthenticatedPermission]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @decorators.action(methods=['post'], detail=False, permission_classes=[], authentication_classes=[])
    def login(self, request):
        phone = request.data.get('phone')
        code = request.data.get('code')
        try:
            # TODO: 验证code
            user = User.objects.get(phone=phone)
        except MultiValueDictKeyError as e:
            raise client_error(f'参数{str(e)}不能为空')
        except User.DoesNotExist:
            user = User(phone=phone)
            user.save()
        if user.is_blocking:
            return fail_response(ERROR_CODE_1001)
        return self.login_success(user)

    @decorators.action(methods=['post'], detail=False)
    def login_password(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')
        user = User.objects.filter(phone=phone).first()
        if not user:
            raise client_error('用户不存在')
        if not user.password:
            raise client_error('密码不存在')
        is_valid = check_password(password, user.password)
        if not is_valid:
            raise client_error('密码错误')
        return self.login_success(user)

    @decorators.action(methods=['post'], url_path='password', detail=True,
                       authentication_classes=[PuppyAuthentication],
                       permission_classes=[IsAuthenticatedPermission])
    def set_password(self, request, _):
        """
        设置密码
        """
        cleartext = request.data.get('password')
        if len(cleartext) <= 8:
            raise client_error('密码错误')
        if request.user.password:
            raise client_error('密码已存在')
        password = make_password(cleartext)
        request.user.password = password
        request.user.save()
        return response.Response(True)

    @decorators.action(methods=['post'], url_path='password/reset', detail=True,
                       authentication_classes=[PuppyAuthentication],
                       permission_classes=[IsAuthenticatedPermission])
    def reset_password(self, request, pk):
        new = request.data.get('new')
        old = request.data.get('old')
        user = request.user
        if new == old:
            raise client_error('新密码和旧密码不能一致')
        if not check_password(old, user.password):
            raise client_error('密码错误')
        password = make_password(new)
        user.password = password
        user.save()
        return response.Response(True)

    @decorators.action(methods=['post'], detail=False, permission_classes=[])
    def logout(self, _):
        return response.Response(True)

    @decorators.action(methods=['get'], detail=True)
    def collections(self, _, pk):
        """
        用户收藏的帖子
        """
        collections = User.objects.prefetch_related('collections').get(pk=pk).collections
        page = self.paginate_queryset(collections)
        serializer = PostSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def login_success(self, user: User):
        token = RefreshToken.for_user(user)
        user.last_login = timezone.localtime()
        user.save()
        return response.Response({'token': str(token.access_token), 'user': LoginUserSerializer(user).data})
