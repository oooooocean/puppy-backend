from rest_framework import viewsets, mixins
from api.common import authentication, permissions
from api.views.base import BaseView
from api.seralizers.user import UserInfoSerializer
from api.models.user import UserInfo


class UserInfoViewSet(BaseView,
                      mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    authentication_classes = [authentication.PuppyAuthentication]
    permission_classes = [permissions.IsAuthenticatedPermission]
    serializer_class = UserInfoSerializer

    def get_object(self):
        return viewsets.generics.get_object_or_404(UserInfo.objects, owner=self.kwargs['user_id'])
