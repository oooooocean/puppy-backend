from rest_framework import viewsets, decorators, response
from ..base import BaseView
from api.models.user.user_info import UserInfoSerializer
from api.models.user.user import User, UserSimpleSerializer
from api.common.permissions import IsAuthenticatedPermission
from api.common.authentication import PuppyAuthentication


class FollowViewSet(BaseView, viewsets.GenericViewSet):
    """
    关注: POST follow/<id>/
    取消关注: DELETE follow/<id>/
    关注列表: GET follow/
    粉丝列表: GET follow/fans/
    """

    serializer_class = UserSimpleSerializer
    queryset = User.objects.all()
    authentication_classes = [PuppyAuthentication]
    permission_classes = [IsAuthenticatedPermission]

    def create(self, request, *args, **kwargs):
        """
        关注
        """
        user_id = self.request.data.get('follow_id', None)
        self.request.user.idols.add(self.queryset.get(pk=user_id))
        return response.Response(True)

    def list(self, request, *args, **kwargs):
        """
        关注列表
        """
        page = self.paginate_queryset(self.request.user.idols.all())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        取消关注
        """
        idol = self.queryset.get(pk=request.data.get('follow_id'))
        request.user.idols.remove(idol)
        return response.Response(True)

    @decorators.action(methods=['GET'], detail=False)
    def fans(self, request):
        """
        粉丝列表
        """
        page = self.paginate_queryset(self.request.user.fans.all())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)